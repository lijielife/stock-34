from openerp import models,api
from datetime import datetime
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp.tools.float_utils import float_compare, float_round


class stock_move(models.Model):
    _inherit = 'stock.move'    
