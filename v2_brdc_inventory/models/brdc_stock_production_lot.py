from odoo import api, fields, models

class brdc_stock_production_lot(models.Model):
    _name = 'brdc.stock.production.lot'
    _rec_name = 'name'
    _description = 'BRDC Stocks'
    _inherits = {'stock.production.lot': 'brdc_stk_prd_lt'}
    # name = fields.Char()

    brdc_stk_prd_lt = fields.Many2one('stock.production.lot','BRDC Stocks')

    name = fields.Char(string="Lot Name / Vault Name / Niche Name")

    stat = [('av', 'Available'),
            ('fp', 'Fully Paid'),
            ('amo', 'Amortized'),
            ('wit', 'Interred'),
            ('fi', 'Fully Interred'),
            ('reserved', 'Reserved'),
            ('ter', 'Terminated')]

    block_number = fields.Char(string="Block Number")
    lot_number = fields.Char(string="Lot Number / Column")
    status = fields.Selection(stat, string="Status", default='av', readonly=False)

    sale_order_id = fields.Many2one('sale.order', string="Ref. No")

    partner_id = fields.Integer(related='sale_order_id.partner_id.id', store=False)
    partner_name = fields.Many2one(string="Policy Holder", related='sale_order_id.partner_id', store=False)

    currency_id = fields.Many2one(related='sale_order_id.currency_id')
    partner_selling_price = fields.Float(string="Selling Price", related='sale_order_id.order_line.price_unit', store=False,)
    partner_contract_price = fields.Monetary(string="Contract Price", related='sale_order_id.amount_total', store=False,)

    # pa_ref = fields.Char(string="Purchase Agreement", related='sale_order_id.pa_ref') # remtemp
    # partner_payment_term =fields.Selection(related='sale_order_id.purchase_term', store=False) # remtemp

    # interred_person = fields.One2many('interment.order2', 'lot_id', limit=2,) # remtemp
    # interment_transaction_id = fields.One2many('sale.order', 'lot_id', domain=[('is_interment', '=', True)]) # remtemp

    product_qty = fields.Float(default=1)
    # allowable_interment = fields.Integer() # remtemp
    is_new = fields.Boolean(default=True)

    # remtemp
    # @api.onchange('product_id')
    # def comp_allowable_interments(self):
    #     if self.product_id.grave_type == "Community Vault":
    #         self.allowable_interment = int(self.product_id.no_of_lot) * 1
    #     elif self.product_id.grave_type == "Columbarium":
    #         self.allowable_interment = int(self.product_id.no_of_lot) * 3
    #     else:
    #         self.allowable_interment = int(self.product_id.no_of_lot) * 2

    # @api.depends('product_id')
    # @api.onchange('product_id', 'block_number', 'lot_number')
    # def set_lot_ser(self):
    #     if self.product_id and self.block_number and self.lot_number:
    #         if self.product_id.categ_id.name == 'Community Vault' or self.product_id.categ_id.name == 'Columbarium':
    #             gt = self.product_id.grave_type
    #             if ' ' in str(gt):
    #                 st = str(gt).split()
    #                 at = ''
    #                 for t in st:
    #                     at = at + t[0:1]
    #                 self.ref = "C" + str(
    #                     self.lot_number) + at
    #                 self.name = " Level" + str(
    #                     self.lot_number) + " " + gt
    #             else:
    #                 self.ref = "C" + str(
    #                     self.lot_number) + str(self.product_id.grave_type)[0:1]
    #                 self.name = " Level" + str(
    #                     self.lot_number) + " " + gt
    #         else:
    #             gt = self.product_id.grave_type
    #             if ' ' in str(gt):
    #                 st = str(gt).split()
    #                 at = ''
    #                 for t in st:
    #                     at = at + t[0:1]
    #                 self.ref = "B" + str(self.block_number) + "L" + str(
    #                     self.lot_number) + at
    #                 self.name = "[" + self.ref + "] " + "Block" + str(self.block_number) + " Lot" \
    #                             + str(self.lot_number) + " " + gt
    #             else:
    #                 self.ref = "B" + str(self.block_number) + "L" + str(
    #                     self.lot_number) + str(self.product_id.grave_type)[0:1]
    #                 self.name = "[" + self.ref + "] " + "Block" + str(self.block_number) + " Lot" \
    #                             + str(self.lot_number) + " " + gt
    #     else:
    #         self.ref = ""
    #         self.name = ""
