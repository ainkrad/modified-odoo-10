from odoo import api, fields, models

class inherited_stock_inventory_line(models.Model):

    _inherit = 'stock.inventory'

    filter = fields.Selection(default='product')

    def import_serials(self):
        block_serial = self.env['stock.inventory.line']
        # print self.env['stock.production.lot'].search_count([('product_id', '=', self.product_id.id)])

        # l_o_p = self.env['stock.production.lot'].search_count([('product_id', '=', self.product_id.id),
        #                                                        ('is_new', '=', True)])

        if self.filter == 'none':
            block_serial.search([('inventory_id', '=', self.id)]).unlink()
            l_o_p = self.env['stock.production.lot'].search([('is_new', '=', True)])
        elif self.filter == 'product':
            block_serial.search([('product_id', '=', self.product_id.id),('inventory_id', '=', self.id)]).unlink()
            l_o_p = self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id),
                                                                         ('is_new', '=', True)])
            # self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id),
            #                                          ('is_new', '=', True)])
        print l_o_p, len(l_o_p)
        for c in range(0, len(l_o_p)):
            # print self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id)])[c-1].id
            line_id = block_serial.create({
                'inventory_id': self.id,
                'company_id': self.company_id.id,
                'product_id': l_o_p[c].product_id.id,
                'prod_lot_id': l_o_p[c].id,
                'location_id': self.location_id.id,
                'product_qty': 1
            })

            line_id.prod_lot_id.is_new = False

    # def set_to_not_new(self):

    # @api.multi
    # def action_done(self):
    #
    #     block_serial = self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id),
    #                                                                      ('is_new', '=', True)])
    #     for c in range(0, len(block_serial)):
    #         block_serial[c].is_new = False
    #
    #     negative = next((line for line in self.mapped('line_ids') if line.product_qty < 0 and line.product_qty != line.theoretical_qty), False)
    #     if negative:
    #         raise UserError(_('You cannot set a negative product quantity in an inventory line:\n\t%s - qty: %s') % (negative.product_id.name, negative.product_qty))
    #     self.action_check()
    #     self.write({'state': 'done'})
    #     self.post_inventory()
    #     return True