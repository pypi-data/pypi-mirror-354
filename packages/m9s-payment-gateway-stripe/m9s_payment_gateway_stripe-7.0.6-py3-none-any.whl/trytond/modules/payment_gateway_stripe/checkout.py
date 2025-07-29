# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import http.client
import json
import logging

from decimal import Decimal

import stripe

from trytond.modules.nereid_checkout.checkout import (
    not_empty_cart, sale_has_non_guest_party, with_company_context)
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

from nereid import (
    Response, abort, current_website, flash, redirect, render_template,
    request, route, url_for)
from nereid.contrib.locale import make_lazy_gettext

_ = make_lazy_gettext('payment_gateway_stripe')

logger = logging.getLogger(__name__)

stripe.api_version = '2024-09-30.acacia'


class Checkout(metaclass=PoolMeta):
    __name__ = 'nereid.checkout'

    @classmethod
    def _process_credit_card_payment(cls, cart, credit_card_form):
        # Validate the credit card form and checkout using that
        # Only one payment per gateway
        gateway = current_website.credit_card_gateway
        if gateway.method == 'credit_card' and gateway.provider == 'stripe':
            sale = cart.sale
            payment = sale._get_payment_for_gateway(gateway)
            if payment is None:
                sale._add_sale_payment(credit_card_form=credit_card_form)
                payment = sale._get_payment_for_gateway(gateway)
            # Update the paymount_amount with the actual needed sum, when
            # it was set to 0 by a cancelation.
            if payment.amount == Decimal('0'):
                payment.amount = sale._get_amount_to_checkout()
                payment.save()
            payment_transaction = payment._create_payment_transaction(
                payment.amount, 'Payment by Card')
            payment_transaction.save()
            payment_transaction.create_payment_intent_stripe()
            client_secret = payment_transaction.provider_token
            sale.save()
            return redirect(url_for('nereid.checkout.stripe_checkout',
                    sale_id=sale.id, client_secret=client_secret))
        else:
            super()._process_credit_card_payment(cart, credit_card_form)

    @classmethod
    @route('/checkout/checkout_stripe/<sale_id>/<client_secret>',
        methods=['GET'])
    @not_empty_cart
    @sale_has_non_guest_party
    @with_company_context
    def stripe_checkout(cls, sale_id=None, client_secret=None):
        pool = Pool()
        Sale = pool.get('sale.sale')

        if not sale_id or not client_secret:
            return
        sale = Sale(sale_id)
        payment_gateway = current_website.credit_card_gateway
        return render_template(
            'checkout/checkout_stripe.jinja',
            sale=sale,
            payment_gateway=payment_gateway,
            client_secret=client_secret,
            )

    @classmethod
    @route('/checkout_stripe_form/<sale_id>/<client_secret>',
        methods=['GET'])
    def stripe_checkout_form(cls, sale_id=None, client_secret=None):
        '''
        Undecorated method allowing the call without cart.
        '''
        pool = Pool()
        Sale = pool.get('sale.sale')

        if not sale_id or not client_secret:
            return
        sale = Sale(sale_id)
        payment_gateway = current_website.credit_card_gateway
        return render_template(
            'checkout/checkout_stripe.jinja',
            sale=sale,
            payment_gateway=payment_gateway,
            client_secret=client_secret,
            )

    @classmethod
    @route('/checkout/stripecancel/<sale_id>', methods=['GET'], readonly=False)
    @with_company_context
    def cancel_stripe_payment(cls, sale_id=None):
        '''
        Set the transaction to failed and return to payment options
        '''
        pool = Pool()
        Sale = pool.get('sale.sale')
        GatewayTransaction = pool.get('payment_gateway.transaction')

        if sale_id:
            sale = Sale(sale_id)
            payment = None
            stripe = current_website.credit_card_gateway
            for s_payment in sale.payments:
                if s_payment.gateway.id == stripe.id:
                    payment = s_payment
                    break
            if payment:
                payment.amount = Decimal('0.0')
                payment.save()
                transactions = GatewayTransaction.search([
                    ('sale_payment', '=', payment.id),
                    ])
                for transaction in transactions:
                    transaction.state = 'cancel'
                    transaction.save()
            flash(_('Credit Card payment canceled'), 'info')
        else:
            flash(_('Error in processing payment.'), 'warning')
        return redirect(url_for('nereid.checkout.payment_method'))

    @classmethod
    @route('/checkout/webhook/stripe/<identifier>', methods=['POST'],
        exempt_csrf=True)
    @with_company_context
    def webhook_endpoint(cls, identifier):
        pool = Pool()
        PaymentGateway = pool.get('payment_gateway.gateway')

        gateway, = PaymentGateway.search([
                ('stripe_webhook_endpoint', 'like', f'%{identifier}'),
                ], limit=1)
        secret = gateway.stripe_webhook_signature_secret_key
        if secret:
            sig_header = request.headers['STRIPE_SIGNATURE']
            request_body = request.get_data(as_text=True)
            try:
                stripe.Webhook.construct_event(
                    request_body, sig_header, secret)
            except ValueError:  # Invalid payload
                abort(http.client.BAD_REQUEST)
            except stripe.error.SignatureVerificationError:
                abort(http.client.BAD_REQUEST)
        else:
            logger.warn("Stripe signature ignored")

        payload = json.loads(request_body)
        result = cls.webhook(payload)
        if result is None:
            logger.info("No callback for payload type '%s'", payload['type'])
        elif not result:
            return Response(status=http.client.NOT_FOUND)
        return Response(status=http.client.NO_CONTENT)

    @classmethod
    def webhook(cls, payload):
        '''
        This method dispatches stripe webhook callbacks

        The return values are:
            - None if there is no method defined to handle the payload type
            - True if the payload has been handled
            - False if the payload could not be handled
        '''
        data = payload['data']
        type_ = payload['type']
        if type_ == 'charge.succeeded':
            return cls.webhook_charge_succeeded(data)
        if type_ == 'charge.captured':
            return cls.webhook_charge_captured(data)
        elif type_ == 'charge.failed':
            return cls.webhook_charge_failed(data)
        elif type_ == 'charge.pending':
            return cls.webhook_charge_pending(data)
        elif type_ == 'charge.refunded':
            return cls.webhook_charge_refunded(data)
        elif type_ == 'charge.dispute.created':
            return cls.webhook_charge_dispute_created(data)
        elif type_ == 'charge.dispute.closed':
            return cls.webhook_charge_dispute_closed(data)
        #elif type_ == 'source.chargeable':
        #    return cls.webhook_source_chargeable(data)
        #elif type_ == 'source.failed':
        #    return cls.webhook_source_failed(data)
        #elif type_ == 'source.canceled':
        #    return cls.webhook_source_canceled(data)
        return None

    @classmethod
    def webhook_charge_succeeded(cls, payload, _event='charge.succeeded'):
        pool = Pool()
        PaymentTransaction = pool.get('payment_gateway.transaction')
        TransactionLog = pool.get('payment_gateway.transaction.log')
        Sale = pool.get('sale.sale')
        PaymentTransaction = pool.get('payment_gateway.transaction')

        charge = payload['object']
        transactions = PaymentTransaction.search([
                ('provider_reference', '=', charge['payment_intent']),
                ('state', '!=', 'posted'),
                ], order=[('create_date', 'DESC')])
        if not transactions:
            logger.error("%s: No Transactions for Payment Intent '%s'", _event,
                charge['payment_intent'])
        # When multiple transactions were found we take the last one.
        elif len(transactions) > 1:
            logger.error("%s: Multiple Transactions for Payment Intent '%s'",
                _event, charge['payment_intent'])
        if transactions:
            transaction = transactions[0]
            with Transaction().set_context(company=transaction.company.id):
                # The webhook can be sent for a former unsuccessful
                # charge (e.g. error in 3D autorisation) which means there can
                # exist failed transcations for the same intent.
                # If we don't find another posted transaction we create a new
                # one that will succeed.
                if transaction.state == 'failed':
                    posted_transactions = PaymentTransaction.search([
                            ('provider_reference', '=',
                                charge['payment_intent']),
                            ('state', '=', 'posted'),
                            ], order=[('create_date', 'DESC')])
                    if not posted_transactions:
                        transaction, = transaction.copy([transaction])
                        transaction.provider_reference = (
                            charge['payment_intent'])
                transaction.charge_id = charge['id']
                transaction.save()
                # Use the queue to post the payment transaction to avoid
                # transaction locking errors.
                with Transaction().set_context(
                        queue_name='stripe_payment_post_processing'):
                    PaymentTransaction.__queue__.batch_post([transaction])
                TransactionLog.create([{
                    'transaction': transaction.id,
                    'log': str(payload),
                }])
            # Reprocess any sales for updated payments
            if isinstance(transaction.origin, Sale):
                sale = transaction.origin
                if (sale.channel_type == 'manual'
                        and sale.state == 'processing'):
                    with Transaction().set_context(
                            queue_name='stripe_payment_post_processing'):
                        Sale.__queue__.queue_express_process(
                            [transaction.origin])

        return bool(transactions)

    @classmethod
    def webhook_charge_captured(cls, payload):
        return cls.webhook_charge_succeeded(payload, _event='charge.captured')

    @classmethod
    def webhook_charge_pending(cls, payload):
        return cls.webhook_charge_succeeded(payload, _event='charge.pending')

    @classmethod
    def webhook_charge_refunded(cls, payload):
        # Let refunds just succeed (#5067)
        # For now we handle refunds manually via web interface and reconcile
        # like all gateway payments against account 1360
        return True
        #return cls.webhook_charge_succeeded(payload, _event='charge.pending')

    @classmethod
    def webhook_charge_failed(cls, payload, _event='charge.failed'):
        pool = Pool()
        PaymentTransaction = pool.get('payment_gateway.transaction')
        TransactionLog = pool.get('payment_gateway.transaction.log')

        charge = payload['object']
        transactions = PaymentTransaction.search([
                ('provider_reference', '=', charge['payment_intent']),
                ('state', '!=', 'posted'),
                ], order=[('create_date', 'DESC')])
        if not transactions:
            logger.error("%s: No Transactions for Payment Intent '%s'", _event,
                charge['payment_intent'])
        elif len(transactions) > 1:
            logger.error("%s: Multiple Transactions for Payment Intent '%s'",
                _event, charge['payment_intent'])
        transaction, = transactions
        with Transaction().set_context(company=transaction.company.id):
            transaction.charge_id = charge['id']
            transaction.state = 'failed'
            transaction.save()
            transaction.delete_move_if_exists()
            TransactionLog.create([{
                'transaction': transaction.id,
                'log': str(payload),
            }])

        # Reset the sale to channel defaults
        sale = transaction.origin
        sale.payment_authorize_on = sale.channel.payment_authorize_on
        sale.payment_capture_on = sale.channel.payment_capture_on
        sale.save()
        return bool(transactions)

    @classmethod
    def webhook_charge_dispute_created(cls, payload):
        pool = Pool()
        PaymentTransaction = pool.get('payment_gateway.transaction')
        TransactionLog = pool.get('payment_gateway.transaction.log')

        source = payload['object']
        transactions = PaymentTransaction.search([
                ('charge_id', '=', source['charge']),
                ], order=[('create_date', 'DESC')])
        if not transactions:
            logger.error(
                "charge.dispute.created: No Transaction for Charge '%s'",
                source['charge'])
        elif len(transactions) > 1:
            logger.error("charge.dispute.created: Multiple Transactions for Charge '%s'",
                source['charge'])
        for transaction in transactions:
            with Transaction().set_context(company=transaction.company.id):
                transaction.dispute_reason = source['reason']
                transaction.dispute_status = source['status']
                transaction.save()
                TransactionLog.create([{
                    'transaction': transaction.id,
                    'log': str(payload),
                }])
        return bool(transactions)

    @classmethod
    def webhook_charge_dispute_closed(cls, payload):
        pool = Pool()
        PaymentTransaction = pool.get('payment_gateway.transaction')
        TransactionLog = pool.get('payment_gateway.transaction.log')

        source = payload['object']
        transactions = PaymentTransaction.search([
                ('charge_id', '=', source['charge']),
                ], order=[('create_date', 'DESC')])
        if not transactions:
            logger.error(
                "charge.dispute.closed: No Transaction for Charge '%s'",
                source['charge'])
        elif len(transactions) > 1:
            logger.error("charge.dispute.closed: Multiple Transactions for Charge '%s'",
                source['charge'])
        for transaction in transactions:
            with Transaction().set_context(company=transaction.company.id):
                transaction.dispute_reason = source['reason']
                transaction.dispute_status = source['status']
                if source['status'] == 'lost':
                    if transaction.stripe_amount != source['amount']:
                        transaction.stripe_amount -= source['amount']
                    else:
                        transaction.state = 'failed'
                transaction.save()

                TransactionLog.create([{
                    'transaction': transaction.id,
                    'log': str(payload),
                }])
        return bool(transactions)

    #@classmethod
    #def webhook_source_chargeable(cls, payload):
    #    pool = Pool()
    #    Payment = pool.get('account.payment')

    #    source = payload['object']
    #    payments = Payment.search([
    #            ('stripe_token', '=', source['id']),
    #            ])
    #    if payments:
    #        Payment.write(payments, {'stripe_chargeable': True})
    #    return True

    #@classmethod
    #def webhook_source_failed(cls, payload):
    #    pool = Pool()
    #    Payment = pool.get('account.payment')

    #    source = payload['object']
    #    payments = Payment.search([
    #            ('stripe_token', '=', source['id']),
    #            ])
    #    for payment in payments:
    #        # TODO: remove when https://bugs.tryton.org/issue4080
    #        with Transaction().set_context(company=payment.company.id):
    #            Payment.fail([payment])
    #    return True

    #@classmethod
    #def webhook_source_canceled(cls, payload):
    #    pool = Pool()
    #    Payment = pool.get('account.payment')

    #    source = payload['object']
    #    payments = Payment.search([
    #            ('stripe_token', '=', source['id']),
    #            ])
    #    for payment in payments:
    #        # TODO: remove when https://bugs.tryton.org/issue4080
    #        with Transaction().set_context(company=payment.company.id):
    #            Payment.fail([payment])
    #    return True
