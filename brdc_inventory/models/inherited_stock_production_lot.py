from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError

class inherited_stock_production_lot(models.Model):

    _inherit = 'stock.production.lot'

    name = fields.Char(string="Lot Name / Niche Name")

    stat = [('av', 'Available'),
            ('fp', 'Fully Paid'),
            ('amo', 'Amortized'),
            ('wit', 'Interred'),
            ('fi', 'Fully Interred'),
            ('reserved', 'Reserved'),
            ('ter', 'Terminated')]

    block_number = fields.Char(string="Block Number")
    lot_number = fields.Char(string="Lot Number / Column Number")
    status = fields.Selection(stat, string="Status", default='av', readonly=False)

    # @api.multi
    # def _get_policy_holder(self):c
    #     related_model_id = self.env['sale.order.line'].search([('lot_id', '=', self.id),('invoice_status', '!=', 'terminated')]).order_id
    #     return related_model_id

    currency_id = fields.Many2one(
        'res.currency', 'Currency', compute='_compute_currency_id')

    sale_order_id = fields.Many2one('sale.order', string="Ref. No")
    pa_ref = fields.Char(string="Purchase Agreement", related='sale_order_id.pa_ref')

    loanee_id = fields.Integer(related='sale_order_id.partner_id.id', store=False)
    loanee_name = fields.Many2one(string="Policy Holder", related='sale_order_id.partner_id', store=False)
    loanee_payment_term =fields.Selection(related='sale_order_id.purchase_term', store=False)
    currency_id = fields.Many2one(related='sale_order_id.currency_id')
    loanee_selling_price = fields.Float(string="Selling Price", related='sale_order_id.order_line.price_unit', store=False,)
    loanee_contract_price = fields.Monetary(string="Contract Price", related='sale_order_id.amount_total', store=False,)
    # loanee_id = fields.Many2one('sale.order')

    interred_person = fields.One2many('interment.order2', 'lot_id', limit=2,)
    eipp_transaction_id = fields.One2many('sale.order', 'lot_id', domain=[('is_interment', '=', True)])

    product_qty = fields.Float(default=1)
    # allowable_interment = fields.Integer(default=comp_allowable_interments)
    allowable_interment = fields.Integer()
    is_new = fields.Boolean(default=True)



    @api.onchange('product_id')
    def comp_allowable_interments(self):
        if self.product_id.grave_type == "Community Vault":
            self.allowable_interment = int(self.product_id.no_of_lot) * 1
        elif self.product_id.grave_type == "Columbarium":
            self.allowable_interment = int(self.product_id.no_of_lot) * 3
        else:
            self.allowable_interment = int(self.product_id.no_of_lot) * 2
        # self.allowable_interment = (int(self.env['product.product'].search([('id', '=', self.product_id.id)]).no_of_lot) * 2)

    @api.onchange('status')
    def onchange_status(self):
        raise UserError(_('Please dont modify the Status of each Lot / Vault / Niches'))

    # @api.onchange('eipp_transaction_id')
    # def set_paid_interment_services(self):
    #     self.paid_interment_services = 1
    #     # self.env['sale.order'].search([('lot_id', '=', self.id)])

    @api.depends('product_id')
    @api.onchange('product_id', 'block_number', 'lot_number')
    def set_lot_ser(self):
        if self.product_id and self.block_number and self.lot_number:
            # if str(self.product_id.default_code)[len(str(self.product_id.default_code))-1:] != "C" and \
            #         str(self.product_id.default_code)[len(str(self.product_id.default_code))-1:] != "V":  # Careful here
            if self.product_id.categ_id.name == 'Community Vault' or self.product_id.categ_id.name == 'Columbarium':
                gt = self.product_id.grave_type
                if ' ' in str(gt):
                    st = str(gt).split()
                    at = ''
                    for t in st:
                        at = at + t[0:1]
                    self.ref = "C" + str(
                        self.lot_number) + at
                    self.name = " Column" + str(
                        self.lot_number) + " " + gt
                else:
                    self.ref = "C" + str(
                        self.lot_number) + str(self.product_id.grave_type)[0:1]
                    self.name = " Column" + str(
                        self.lot_number) + " " + gt
            else: # ^V
                gt = self.product_id.grave_type
                if ' ' in str(gt):
                    st = str(gt).split()
                    at = ''
                    for t in st:
                        at = at + t[0:1]
                    self.ref = "B" + str(self.block_number) + "L" + str(
                        self.lot_number) + at
                    self.name = "[" + self.ref + "] " + "Block" + str(self.block_number) + " Lot" \
                                + str(self.lot_number) + " " + gt
                else:
                    self.ref = "B" + str(self.block_number) + "L" + str(
                        self.lot_number) + str(self.product_id.grave_type)[0:1]
                    self.name = "[" + self.ref + "] " + "Block" + str(self.block_number) + " Lot" \
                                + str(self.lot_number) + " " + gt

                # gt = self.product_id.grave_type
                # if ' ' in str(gt):
                #     st = str(gt).split()
                #     at = ''
                #     for t in st:
                #         at = at + t[0:1]
                #     self.ref = "L" + str(self.block_number) + "C" + str(
                #         self.lot_number) + at
                #     self.name = "[" + self.ref + "] " + "Layer" + str(self.block_number) + " Column" + str(
                #         self.lot_number) + " " + gt
                # else:
                #     self.ref = "L" + str(self.block_number) + "C" + str(
                #         self.lot_number) + str(self.product_id.grave_type)[0:1]
                #     self.name = "[" + self.ref + "] " + "Layer" + str(self.block_number) + " Column" + str(
                #         self.lot_number) + " " + gt
        else:
            self.ref = ""
            self.name = ""
