from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class inherited_stock_pack_operation(models.Model):

    _inherit = 'stock.pack.operation'

    def validate_inv(self):


        lot = self.env['sale.order'].search([('name', '=', self.env['stock.picking'].
                                              search([('id', '=', self.picking_id.id)]).origin)]).lot_id
        lot.status = 'reserved'
        # lot = self.env['sale.order'].search([('name', '=', self.env['stock.picking'].
        #                                       search([('id', '=', self.picking_id.id)]).origin)]).order_line.lot_id
        # for c in range(0, len(lot)):
        #     lot[c].status = 'reserved'
        # lot.sale_order_id = self.env['sale.order'].search([('name', '=', self.env['stock.picking'].
        #                                       search([('id', '=', self.picking_id.id)]).origin)]).order_line.id


        # lot.loanee_id = self.env['stock.picking'].search([('id', '=', self.picking_id.id)]).partner_id.id

        self.qty_done = 1
        block_serial = self.env['stock.pack.operation.lot']
        block_serial.search([('operation_id', '=', self.id)]).unlink()

        line_id = block_serial.create({
            'operation_id': self.id,
            'qty': 1,
            'lot_id': self.env['sale.order'].search([('name', '=', self.env['stock.picking'].search([('id', '=', self.picking_id.id)]).origin
                                                      )]).lot_id.id,
            'lot_name': self.env['sale.order'].search(
                [('name', '=', self.env['stock.picking'].search([('id', '=', self.picking_id.id)]).origin
                  )]).lot_id.name,
            'loc_det_id': self.to_loc
        })

        # 'lot_id': self.env['sale.order'].search(
        #     [('name', '=', self.env['stock.picking'].search([('id', '=', self.picking_id.id)]).origin
        #       )]).order_line.lot_id.id,
        # 'lot_name': self.env['sale.order'].search(
        #     [('name', '=', self.env['stock.picking'].search([('id', '=', self.picking_id.id)]).origin
        #       )]).order_line.lot_id.name,

    # @api.model
    # def create(self, vals):
    #
    #     block_serial = self.env['stock.pack.operation.lot']
    #     block_serial.search([('operation_id', '=', self.id)]).unlink()
    #
    #     line_id = block_serial.create({
    #         'operation_id': self.id,
    #         'qty': 1,
    #         'lot_id': self.env['sale.order'].
    #             search([('name', '=', self.env['stock.picking'].
    #                                                   search([('id', '=', self.env['stock.pack.operation'].
    #                                                            search([('id', '=', self.operation_id.id)]).picking_id.id
    #                                                   )]).origin)]).order_line.lot_id.id,
    #         # 'lot_name': self.env['sale.order'].search(
    #         #     [('name', '=', self.env['stock.picking'].search([('id', '=', self.picking_id.id)]).origin
    #         #       )]).order_line.lot_id.name,
    #     })
    #     return super(inherited_stock_pack_operation, self).create(vals)

class inherited_stock_picking(models.Model):

    _inherit = 'stock.picking'

    def set_lot(self):
        block_serial = self.env['stock.pack.operation'].search([('picking_id', '=', self.id)]).validate_inv()

    def do_new_transfer(self):
     # print self.env['sale.order'].search([('name','=',self.origin)]).invoice_status,self.env['sale.order'].search([('name','=',self.origin)])[0].name

        if self.env['sale.order'].search([('name','=',self.origin)])[0].name == self.origin:
            print "im here"
            if self.env['sale.order'].search([('name','=',self.origin)]).invoice_status != 'invoiced':
                raise UserError(_('Please provide one or more payments'))
            else:
                pass
            print self.env['sale.order'].search([('name', '=', self.origin)])[0].lot_id, self.env[
                'sale.order'].search([('name', '=', self.origin)]).id

            self.env['sale.order'].search([('name', '=', self.origin)])[0].lot_id.sale_order_id = self.env[
                'sale.order'].search([('name', '=', self.origin)]).id
        else:
            pass
        # print self.env['sale.order'].search([('name', '=', self.origin)]).order_line.id, self.env['sale.order'].search([('name', '=', self.origin)]).lot_id


        # lot = self.env['sale.order'].search([('name', '=', self.origin)]).order_line.lot_id
        # heres the old
        # for c in range(1, self.env['stock.pack.operation.lot'].search_count([('operation_id', '=',
        #                                                                       self.env['stock.pack.operation'].
        #                                                                               search([('picking_id', '=',
        #                                                                                        self.id)]).id)]) + 1):
        #
        #
        #     lot = self.env['stock.pack.operation.lot'].search([('operation_id', '=',
        #                                                         self.env['stock.pack.operation'].
        #                                                         search([('picking_id', '=',
        #                                                                  self.id)]).id)])
        #     # print lot
        #     # lot[c-1].lot_id.status = 'reserved'
        #
        #     lot[c-1].lot_id.sale_order_id = self.env['sale.order'].search([('name', '=', self.origin)]).order_line.id
        #up to here
        # self.env['sale.order'].search(
        #     [('name', '=', self.env['stock.picking'].search([('id', '=', self.picking_id.id)]).origin
        #       )]).order_line.lot_id.status = 'fp'
        # block_serial = self.env['stock.pack.operation'].search([('picking_id', '=', self.id)]).validate_inv()

        for pick in self:
            if pick.state == 'done':
                raise UserError(_('The pick is already validated'))
            pack_operations_delete = self.env['stock.pack.operation']
            if not pick.move_lines and not pick.pack_operation_ids:
                raise UserError(_('Please create some Initial Demand or Mark as Todo and create some Operations. '))
            # In draft or with no pack operations edited yet, ask if we can just do everything
            if pick.state == 'draft' or all([x.qty_done == 0.0 for x in pick.pack_operation_ids]):
                # If no lots when needed, raise error
                picking_type = pick.picking_type_id
                if (picking_type.use_create_lots or picking_type.use_existing_lots):
                    for pack in pick.pack_operation_ids:
                        if pack.product_id and pack.product_id.tracking != 'none':
                            raise UserError(_('Some products require lots/serial numbers, so you need to specify those first!'))
                view = self.env.ref('stock.view_immediate_transfer')
                wiz = self.env['stock.immediate.transfer'].create({'pick_id': pick.id})
                # TDE FIXME: a return in a loop, what a good idea. Really.
                return {
                    'name': _('Immediate Transfer?'),
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'stock.immediate.transfer',
                    'views': [(view.id, 'form')],
                    'view_id': view.id,
                    'target': 'new',
                    'res_id': wiz.id,
                    'context': self.env.context,
                }

            # Check backorder should check for other barcodes
            if pick.check_backorder():
                view = self.env.ref('stock.view_backorder_confirmation')
                wiz = self.env['stock.backorder.confirmation'].create({'pick_id': pick.id})
                # TDE FIXME: same reamrk as above actually
                return {
                    'name': _('Create Backorder?'),
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'stock.backorder.confirmation',
                    'views': [(view.id, 'form')],
                    'view_id': view.id,
                    'target': 'new',
                    'res_id': wiz.id,
                    'context': self.env.context,
                }
            for operation in pick.pack_operation_ids:
                if operation.qty_done < 0:
                    raise UserError(_('No negative quantities allowed'))
                if operation.qty_done > 0:
                    operation.write({'product_qty': operation.qty_done})
                else:
                    pack_operations_delete |= operation
            if pack_operations_delete:
                pack_operations_delete.unlink()
        self.do_transfer()
        return