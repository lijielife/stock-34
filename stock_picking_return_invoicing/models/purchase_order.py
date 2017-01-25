# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields, _
from openerp.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    should_be_invoiced = fields.Boolean(string="Should be Invoiced", compute="_compute_should_be_invoiced", store=True, default=False)

    @api.multi
    @api.depends('order_line', 'order_line.qty_to_invoice')
    def _compute_should_be_invoiced(self):
        for order in self:
            order.should_be_refunded = False
            for line in order.order_line:
                if line.qty_to_invoice > 0:
                    order.should_be_refunded = True
                    break
    
    @api.multi
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a purchase order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        journal_id = self.env['account.invoice'].default_get(['journal_id'])['journal_id']
        if not journal_id:
            raise UserError(_('Please define an accounting sale journal for this company.'))
        invoice_vals = {
            'name': self.client_order_ref or '',
            'origin': self.name,
            'type': 'in_invoice',
            'account_id': self.partner_id.property_account_expense_id.id,
            'partner_id': self.partner_id.id,
            'journal_id': journal_id,
            'currency_id': self.currency_id.id,
            'comment': self.note,
            'payment_term_id': self.payment_term_id.id,
            'fiscal_position_id': self.fiscal_position_id.id or self.partner_id.property_account_position_id.id,
            'company_id': self.company_id.id,
            'user_id': self.user_id and self.user_id.id,
        }
        return invoice_vals
    
    @api.multi
    def action_invoice_create(self):
        _logger.debug("Create Invoice")
        for order in self:
            # Should not be invoiced
            if not order.should_be_invoiced:
                raise UserError(_('There is no invoicable line.'))

            # Should be invoiced
            """
            Create the invoice associated to the PO.
            :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                            (partner_invoice_id, currency)
            :param final: if True, refunds will be generated if necessary
            :returns: list of created invoices
            """
            inv_obj = self.env['account.invoice']
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            invoices = {}

            for order in self:
                group_key = order.id if grouped else (order.partner_id.id, order.currency_id.id)
                for line in order.order_line.sorted(key=lambda l: l.qty_to_invoice < 0):
                    if float_is_zero(line.qty_to_invoice, precision_digits=precision):
                        continue
                    if group_key not in invoices:
                        inv_data = order._prepare_invoice()
                        invoice = inv_obj.create(inv_data)
                        invoices[group_key] = invoice
                    elif group_key in invoices:
                        vals = {}
                        if order.name not in invoices[group_key].origin.split(', '):
                            vals['origin'] = invoices[group_key].origin + ', ' + order.name
                        if order.client_order_ref and order.client_order_ref not in invoices[group_key].name.split(', '):
                            vals['name'] = invoices[group_key].name + ', ' + order.client_order_ref
                        invoices[group_key].write(vals)
                    if line.qty_to_invoice > 0:
                        line.invoice_line_create(invoices[group_key].id, line.qty_to_invoice)
                    elif line.qty_to_invoice < 0 and final:
                        line.invoice_line_create(invoices[group_key].id, line.qty_to_invoice)

            if not invoices:
                raise UserError(_('There is no invoicable line.'))

            for invoice in invoices.values():
                if not invoice.invoice_line_ids:
                    raise UserError(_('There is no invoicable line.'))
                # If invoice is negative, do a refund invoice instead
                if invoice.amount_untaxed < 0:
                    invoice.type = 'in_refund'
                    for line in invoice.invoice_line_ids:
                        line.quantity = -line.quantity
                # Use additional field helper function (for account extensions)
                for line in invoice.invoice_line_ids:
                    line._set_additional_fields(invoice)
                # Necessary to force computation of taxes. In account_invoice, they are triggered
                # by onchanges, which are not triggered when doing a create.
                invoice.compute_taxes()

            return [inv.id for inv in invoices.values()]
