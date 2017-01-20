from openerp import models,api
from datetime import datetime
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp.tools.float_utils import float_compare, float_round


class stock_move(models.Model):
    _inherit = 'stock.move'

    def check_tracking_product(self, cr, uid, product, lot_id, location, location_dest, context=None):
        check = False
        if product.track_all and not location_dest.usage == 'inventory':
            check = True
        elif product.track_incoming and location.usage in ('supplier', 'transit', 'inventory') and location_dest.usage == 'internal':
            check = True
        elif product.track_outgoing and location_dest.usage in ('customer', 'transit') and location.usage == 'internal':
            check = True
        if check and not lot_id:
            raise osv.except_osv(_('Warning!'), _('You must assign a serial number for the product %s') % (product.name))


    def check_tracking(self, cr, uid, move, lot_id, context=None):
        """ Checks if serial number is assigned to stock move or not and raise an error if it had to.
        """
        self.check_tracking_product(cr, uid, move.product_id, lot_id, move.location_id, move.location_dest_id, context=context)