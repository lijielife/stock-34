# -*- coding: utf-8 -*-

from openerp import models, fields, api

class sale_order_mandatory_delivery_method(models.Model):
    _inherit = 'sale.order'

    carrier_id = fields.Many2one("delivery.carrier", string="Delivery Method", help="Fill this field if you plan to invoice the shipping based on picking.", required=True)