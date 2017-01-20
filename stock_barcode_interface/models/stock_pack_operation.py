from openerp import models

class stock_pack_operation_stock_barcode_interface(models.Model):
    _inherit = 'stock.pack.operation'

    def _search_and_increment(self, cr, uid, picking_id, domain, filter_visible=False, visible_op_ids=False, increment=True, context=None):
        '''Search for an operation with given 'domain' in a picking, if it exists increment the qty (+1) otherwise create it

        :param domain: list of tuple directly reusable as a domain
        context can receive a key 'current_package_id' with the package to consider for this operation
        returns True
        '''
        if context is None:
            context = {}

        #if current_package_id is given in the context, we increase the number of items in this package
        package_clause = [('result_package_id', '=', context.get('current_package_id', False))]
        existing_operation_ids = self.search(cr, uid, [('picking_id', '=', picking_id)] + domain + package_clause, context=context)
        todo_operation_ids = []
        if existing_operation_ids:
            if filter_visible:
                todo_operation_ids = [val for val in existing_operation_ids if val in visible_op_ids]
            else:
                todo_operation_ids = existing_operation_ids
        if todo_operation_ids:
            #existing operation found for the given domain and picking => increment its quantity
            operation_id = todo_operation_ids[0]
            op_obj = self.browse(cr, uid, operation_id, context=context)
            qty = op_obj.qty_done
            if increment:
                qty += 1
            else:
                qty -= 1 if qty >= 1 else 0
                if qty == 0 and op_obj.product_qty == 0:
                    #we have a line with 0 qty set, so delete it
                    self.unlink(cr, uid, [operation_id], context=context)
                    return False
            self.write(cr, uid, [operation_id], {'qty_done': qty}, context=context)
        else:
            #no existing operation found for the given domain and picking => create a new one
            picking_obj = self.pool.get("stock.picking")
            picking = picking_obj.browse(cr, uid, picking_id, context=context)
            values = {
                'picking_id': picking_id,
                'product_qty': 0,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
                'qty_done': 1,
                }
            for key in domain:
                var_name, dummy, value = key
                uom_id = False
                if var_name == 'product_id':
                    uom_id = self.pool.get('product.product').browse(cr, uid, value, context=context).uom_id.id
                update_dict = {var_name: value}
                if uom_id:
                    update_dict['product_uom_id'] = uom_id
                values.update(update_dict)
            operation_id = self.create(cr, uid, values, context=context)
        return operation_id

    def action_drop_down(self, cr, uid, ids, context=None):
        ''' Used by barcode interface to say that pack_operation has been moved from src location 
            to destination location, if qty_done is less than product_qty than we have to split the
            operation in two to process the one with the qty moved
        '''
        processed_ids = []
        move_obj = self.pool.get("stock.move")
        for pack_op in self.browse(cr, uid, ids, context=None):
            if pack_op.product_id and pack_op.location_id and pack_op.location_dest_id:
                move_obj.check_tracking_product(cr, uid, pack_op.product_id, pack_op.lot_id.id, pack_op.location_id, pack_op.location_dest_id, context=context)
            op = pack_op.id
            if pack_op.qty_done < pack_op.product_qty:
                # we split the operation in two
                op = self.copy(cr, uid, pack_op.id, {'product_qty': pack_op.qty_done, 'qty_done': pack_op.qty_done}, context=context)
                self.write(cr, uid, [pack_op.id], {'product_qty': pack_op.product_qty - pack_op.qty_done, 'qty_done': 0}, context=context)
            processed_ids.append(op)
        self.write(cr, uid, processed_ids, {'processed': 'true'}, context=context)