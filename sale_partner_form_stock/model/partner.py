from openerp import models, fields, api, _

class partner_with_stock(models.Model):
    _inherit = ['res.partner']

    open_deliveries_count = fields.Integer(string="Products to deliver", compute="_compute_products_to_deliver")

    @api.one
    def _compute_products_to_deliver(self):
        cr = self.env.cr
        uid = self.env.user.id

        stock_picking_obj = self.pool.get('stock.picking')
        stock_picking_type_obj = self.pool.get('stock.picking.type')
        stock_picking_type_ids = stock_picking_type_obj.search(cr, uid, [('code','=','outgoing')],)

        picking_ids = stock_picking_obj.search(cr, uid, [('partner_id','=',self.id),('picking_type_id','in',stock_picking_type_ids),('state','in',['confirmed','partially_available'])], order="date desc")

        nb = 0
        if picking_ids:
            for picking in stock_picking_obj.browse(cr, uid, picking_ids):
                for move in picking.move_lines:
                    nb += move.product_uom_qty

        self.open_deliveries_count = nb
        