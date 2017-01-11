# -*- encoding: utf-8 -*-
# This code has been written
# by AbAKUS it-solutions PGmbH
# in Belgium, 2015

from openerp import models, fields, api, _
import time
import datetime
import logging
_logger = logging.getLogger(__name__)

class stock_inventory_report(models.TransientModel):

    _name = 'stock.inventory.report'
    date_from = fields.Date("Date from", required=True, default=lambda *a: time.strftime('%Y-%m-%d'))
    date_to = fields.Date("Date to", required=True, default=lambda *a: time.strftime('%Y-%m-%d'))
    location_id = fields.Many2one('stock.location', 'Location', required=True)
    
    #_defaults = {
     #          'date_from': lambda *a: time.strftime('%Y-%m-%d'),
    #           'date_to': lambda *a: time.strftime('%Y-%m-%d'),
    #           }

    def print_report(self, cr, uid, ids, context=None):
        return self.pool.get('report').get_action(cr, uid, ids[0], 'stock_inventory_on_time.stock_inventory_on_time_document', context=context)

        if context is None:
            context = {}
        datas = {
            'ids': context.get('active_ids', []),
            'model': 'stock.inventory.report',
        }

        res = self.read(cr, uid, ids, ['date_from', 'location_id', 'date_to'], context=context)
        res = res and res[0] or {}
        #res['products'] = self.get_datas(cr, date_from, date_to, location)
        datas['form'] = res

        _logger.debug("\n\n\nDatas: %s\n\n\n", datas)

        return {
                   'type': 'ir.actions.report.xml',
                   'report_name': 'stock_inventory_on_time.stock_inventory_on_time_document',
                   'form': datas,
            }  

    def get_report_data(self):
        cr = self.env.cr
        uid = self.env.user.id

        date_start = self.date_from
        date_end = self.date_to
        location_outsource = self.location_id.id

        result = []
        list_product = []
        
        sql_dk = '''SELECT product_id,name, code, sum(product_qty_in - product_qty_out) as qty_dk
                FROM  (SELECT sm.product_id,pt.name , pp.default_code as code,
                    COALESCE(sum(sm.product_qty),0) AS product_qty_in,
                    0 AS product_qty_out
                FROM stock_picking sp
                LEFT JOIN stock_move sm ON sm.picking_id = sp.id
                LEFT JOIN product_product pp ON sm.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN stock_location sl ON sm.location_id = sl.id
                WHERE date_trunc('day',sm.date) < '%s'
                AND sm.state = 'done'
                --AND sp.location_type = 'outsource_out'
                AND sm.location_id <> %s
                AND sm.location_dest_id = %s
                --AND usage like 'internal'
                GROUP BY sm.product_id,
                pt.name ,
                pp.default_code
                UNION ALL
                SELECT sm.product_id,pt.name , pp.default_code as code,
                    0 AS product_qty_in,
                    COALESCE(sum(sm.product_qty),0) AS product_qty_out
                FROM stock_picking sp
                LEFT JOIN stock_move sm ON sm.picking_id = sp.id
                LEFT JOIN product_product pp ON sm.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN stock_location sl ON sm.location_id = sl.id
                WHERE date_trunc('day',sm.date) <'%s'
                AND sm.state = 'done'
                --AND sp.location_type = 'outsource_in'
                AND sm.location_id = %s
                AND sm.location_dest_id <> %s
                --AND usage like 'internal'
                GROUP BY sm.product_id,
                pt.name ,
                pp.default_code) table_dk GROUP BY product_id,name ,code
                    ''' % (date_start, location_outsource,location_outsource, date_start, location_outsource,location_outsource)

        sql_in_tk = '''
            SELECT sm.product_id,pt.name , pp.default_code as code,
                    COALESCE(sum(sm.product_qty),0) AS qty_in_tk
                FROM stock_picking sp
                LEFT JOIN stock_move sm ON sm.picking_id = sp.id
                LEFT JOIN product_product pp ON sm.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN stock_location sl ON sm.location_id = sl.id
                WHERE date_trunc('day',sm.date) >= '%s'
                AND date_trunc('day',sm.date) <= '%s'
                AND sm.state = 'done'
                --AND sp.location_type = 'outsource_out'
                AND sm.location_id <> %s
                AND sm.location_dest_id = %s
                --AND usage like 'internal'
                GROUP BY sm.product_id,
                pt.name ,
                pp.default_code
        '''% (date_start, date_end, location_outsource,location_outsource)

        sql_out_tk = '''
            SELECT sm.product_id,pt.name , pp.default_code as code,
                    COALESCE(sum(sm.product_qty),0) AS qty_out_tk
                FROM stock_picking sp
                LEFT JOIN stock_move sm ON sm.picking_id = sp.id
                LEFT JOIN product_product pp ON sm.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN stock_location sl ON sm.location_id = sl.id
                WHERE date_trunc('day',sm.date) >= '%s'
                AND date_trunc('day',sm.date) <= '%s'
                AND sm.state = 'done'
                --AND sp.location_type = 'outsource_out'
                AND sm.location_id = %s
                AND sm.location_dest_id <> %s
                --AND usage like 'internal'
                GROUP BY sm.product_id,
                pt.name ,
                pp.default_code
        '''% (date_start, date_end, location_outsource,location_outsource)

        sql_ck = '''SELECT product_id,name, code, sum(product_qty_in - product_qty_out) as qty_ck
                FROM  (SELECT sm.product_id,pt.name , pp.default_code as code,
                    COALESCE(sum(sm.product_qty),0) AS product_qty_in,
                    0 AS product_qty_out
                FROM stock_picking sp
                LEFT JOIN stock_move sm ON sm.picking_id = sp.id
                LEFT JOIN product_product pp ON sm.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN stock_location sl ON sm.location_id = sl.id
                WHERE date_trunc('day',sm.date) <= '%s'
                AND sm.state = 'done'
                --AND sp.location_type = 'outsource_out'
                AND sm.location_id <> %s
                AND sm.location_dest_id = %s
                --AND usage like 'internal'
                GROUP BY sm.product_id,
                pt.name ,
                pp.default_code
                UNION ALL
                SELECT sm.product_id,pt.name , pp.default_code as code,
                    0 AS product_qty_in,
                    COALESCE(sum(sm.product_qty),0) AS product_qty_out
                FROM stock_picking sp
                LEFT JOIN stock_move sm ON sm.picking_id = sp.id
                LEFT JOIN product_product pp ON sm.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN stock_location sl ON sm.location_id = sl.id
                WHERE date_trunc('day',sm.date) <='%s'
                AND sm.state = 'done'
                --AND sp.location_type = 'outsource_in'
                AND sm.location_id = %s
                AND sm.location_dest_id <> %s
                --AND usage like 'internal'
                GROUP BY sm.product_id,
                pt.name ,
                pp.default_code) table_ck GROUP BY product_id,name ,code
                    ''' % (date_end, location_outsource,location_outsource, date_end, location_outsource,location_outsource)

        sql = '''
            SELECT ROW_NUMBER() OVER(ORDER BY table_ck.code DESC) AS num ,
                    table_ck.product_id, table_ck.name, table_ck.code,
                    COALESCE(sum(qty_dk),0) as qty_dk,
                    COALESCE(sum(qty_in_tk),0) as qty_in_tk,
                    COALESCE(sum(qty_out_tk),0) as qty_out_tk,
                    COALESCE(sum(qty_ck),0)  as qty_ck
            FROM  (%s) table_ck
                LEFT JOIN (%s) table_in_tk on table_ck.product_id = table_in_tk.product_id
                LEFT JOIN (%s) table_out_tk on table_ck.product_id = table_out_tk.product_id
                LEFT JOIN (%s) table_dk on table_ck.product_id = table_dk.product_id
                GROUP BY table_ck.product_id, table_ck.name, table_ck.code
        ''' %(sql_ck,sql_in_tk, sql_out_tk, sql_dk)
        cr.execute(sql)
        data = cr.dictfetchall()
        for i in data:
            list_product.append({   'num': i['num'],
                                    'name': i['name'],
                                    'code': i['code'],
                                    'qty_dk': i['qty_dk'],
                                    'qty_in_tk': i['qty_in_tk'],
                                    'qty_out_tk': i['qty_out_tk'],
                                    'qty_ck': i['qty_ck'],
                                 })
        return list_product 
