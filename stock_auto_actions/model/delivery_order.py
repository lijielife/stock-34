from openerp import models, fields
import logging

_logger = logging.getLogger(__name__)

class delivery_order(models.Model):
    _inherit = 'stock.picking'

    printed = fields.Boolean(string="Sent to the printed", store=True)

    def cron_action(self, cr, uid, ids=None, context=None):
        picking_obj = self.pool.get('stock.picking')
        waiting_pickings_id = picking_obj.search(cr, uid, [('picking_type_id', '=', 6), ('state','=','confirmed')])
        ready_pickings_id = picking_obj.search(cr, uid, [('picking_type_id', '=', 6), ('state','=','assigned')])

        # Check availability for waiting pickings
        if waiting_pickings_id:
            for pick in picking_obj.browse(cr, uid, waiting_pickings_id):
                picking_obj.action_assign(cr, uid, pick.id, context=context)

        # Check if printed, if not print and set as it
        if ready_pickings_id:
            for pick in picking_obj.browse(cr, uid, ready_pickings_id):
                if (pick.printed == False):
                    pick.write({'printed' : True})
                    picking_obj.pool.get("report").get_action(cr, uid, pick, 'stock.report_picking', context=context)
            