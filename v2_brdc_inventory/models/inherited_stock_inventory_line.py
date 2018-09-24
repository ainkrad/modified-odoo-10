from odoo import api, fields, models

class inherited_stock_inventory_line(models.Model):

    _inherit = 'stock.inventory'

    # filter = fields.Selection(default='product')

    def import_serials(self):
        block_serial = self.env['stock.inventory.line']

        if self.filter == 'none':
            block_serial.search([('inventory_id', '=', self.id)]).unlink()
            l_o_p = self.env['brdc.stock.production.lot'].search([('is_new', '=', True)])
        elif self.filter == 'product':
            block_serial.search([('product_id', '=', self.product_id.id),('inventory_id', '=', self.id)]).unlink()
            l_o_p = self.env['brdc.stock.production.lot'].search([('product_id', '=', self.product_id.id),
                                                                         ('is_new', '=', True)])
        print l_o_p, len(l_o_p)
        for c in range(0, len(l_o_p)):
            line_id = block_serial.create({
                'inventory_id': self.id,
                'company_id': self.company_id.id,
                'product_id': l_o_p[c].product_id.id,
                'prod_lot_id': l_o_p[c].id,
                'location_id': self.location_id.id,
                'product_qty': 1
            })

            line_id.prod_lot_id.is_new = False
