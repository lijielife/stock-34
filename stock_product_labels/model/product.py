from openerp import models, fields, api
from openerp.osv import osv
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class product_with_stock_label(models.Model):
    _inherit = ['product.template']

    @api.multi
    def print_labels(self):
        if len(self.product_variant_ids) < 1:
            raise osv.except_osv(_("There is no variant!"), _("Impossible to print labels while there is no variant defined"))
        table = []
        for variant in self.product_variant_ids:
            table.append(variant.id)
        return self.pool['report'].get_action(self.env.cr, self.env.uid, table, 'stock_product_labels.product_label', context=self.env.context)

    @api.multi
    def print_labels_with_stock_location(self):
        if len(self.product_variant_ids) < 1:
            raise osv.except_osv(_("There is no variant!"), _("Impossible to print labels while there is no variant defined"))
        print_ids = []
        for variant in self.product_variant_ids:
            stock_quants_obj = self.pool.get('stock.quant')
            stock_quants_ids = stock_quants_obj.search(self.env.cr, self.env.uid, [('product_id', '=', variant.id)])
            if len(stock_quants_ids) > 0:
                for i in stock_quants_ids:
                    print_ids.append(i)
        if len(print_ids) < 1:
            raise osv.except_osv(_("No Variant in stock."), _("Impossible to print the stock location for this products because there is none in stock. Use the other button for simple labels"))

        return self.pool['report'].get_action(self.env.cr, self.env.uid, print_ids, 'stock_product_labels.product_label_stock', context=self.env.context)