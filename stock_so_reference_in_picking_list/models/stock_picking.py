# -*- coding: utf-8 -*-

from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class stock_picking_with_customer_so_reference(models.Model):
    _inherit = 'stock.picking'

    customer_reference = fields.Char(string="Reference/Description (from SO)", compute="_compute_customer_reference")

    @api.multi
    def _compute_customer_reference(self):
        for l in self:
            order = self.env['sale.order'].search([('partner_id', '=', l.partner_id.id), ('name', '=', l.group_id.name)])
            l.customer_reference = order.client_order_ref
