from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError

class lot_generator_handler(models.TransientModel):
    _name = 'lot.generator'
    # _rec_name = 'name'
    _description = 'Lot Generator'

    product_id = fields.Many2one('product.product', string="Product", required=True, domain=[('type','=','product')])

    no_of_blocks = fields.Integer(string="No of Blocks per Area", default=0, required=True)
    no_of_lots = fields.Integer(string="No of Lots per Block", default=0, required=True)

    lot_temp_id = fields.One2many('lot.temp', 'lot_gen_id')

    state = fields.Selection([
        ('draft', "Draft"),
        ('gen', "Generated"),
        ('create', "Create"),
    ], default='draft')

    def ir_n_name(self, prod_id, c, d):
        if prod_id.categ_id.name == 'Community Vault' or prod_id.categ_id.name == 'Columbarium':
            gt = prod_id.grave_type
            if ' ' in str(gt):
                st = str(gt).split()
                at = ''
                for t in st:
                    at = at + t[0:1]
                ref = "C" + str(
                    d) + at
                name = " Column" + str(
                    d) + " " + gt
            else:
                ref = "C" + str(
                    d) + str(prod_id.grave_type)[0:1]
                name = " Column" + str(
                    d) + " " + gt
        else:  # ^V
            gt = prod_id.grave_type
            if ' ' in str(gt):
                st = str(gt).split()
                at = ''
                for t in st:
                    at = at + t[0:1]
                ref = "B" + str(c) + "L" + str(
                    d) + at
                name = "[" + ref + "] " + "Block" + str(c) + " Lot" \
                            + str(d) + " " + gt
            else:
                ref = "B" + str(c) + "L" + str(
                    d) + str(prod_id.grave_type)[0:1]
                name = "[" + ref + "] " + "Block" + str(c) + " Lot" \
                            + str(d) + " " + gt
        return name, ref

    # @api.onchange('product_id')
    def comp_allowable_interments(self):
        if self.product_id.grave_type == "Community Vault":
            all_int = int(self.product_id.no_of_lot) * 1
        elif self.product_id.grave_type == "Columbarium":
            all_int = int(self.product_id.no_of_lot) * 3
        else:
            all_int = int(self.product_id.no_of_lot) * 2
        return all_int

    @api.multi
    def action_draft(self):
        self.state = 'draft'
        # self.lot_id.status = 'av'
        # self.env['lot.generator'].search([('id', '=', self.id)]).unlink()
        return {
            "type": "ir.actions.do_nothing",
        }
    @api.multi
    def action_generate(self):
        self.state = 'gen'
        if (self.product_id.grave_type == "Columbarium" or self.product_id.grave_type == "Community Vault")and self.no_of_blocks > 1:
            raise UserError(_('Blocks per Area must not be greater than 1'))

        for c in range(1, self.no_of_blocks + 1):
            for d in range(1, self.no_of_lots + 1):
                generate_blocklots = self.env['lot.temp']
                # generate_blocklots.unlink()

                if not self.env['lot.temp'].search([('block_no', '=', c),('lot_no','=',d),('lot_gen_id','=',self.id)]):
                    line_id = generate_blocklots.create({
                        'block_no': c,
                        'lot_no': d,
                        'stat': 'av',
                        'lot_gen_id': self.id,
                    })

        return {
            "type": "ir.actions.do_nothing",
        }

    @api.multi
    def action_create(self):
        self.state = 'create'
        prod_id = self.product_id
        for x in range(0,len(self.lot_temp_id)):
                if self.product_id.categ_id.name == 'Community Vault' or self.product_id.categ_id.name == 'Columbarium':
                    create_blocklots = self.env['stock.production.lot']
                    line_id = create_blocklots.create({
                        'block_number': " ",
                        'lot_number': self.lot_temp_id[x].lot_no,
                        'name': self.ir_n_name(prod_id, self.lot_temp_id[x].block_no, self.lot_temp_id[x].lot_no)[0],
                        'ref': self.ir_n_name(prod_id, self.lot_temp_id[x].block_no, self.lot_temp_id[x].lot_no)[1],
                        'status': self.lot_temp_id[x].status,
                        'product_id': prod_id.id,
                        'is_new': True,
                        'allowable_interment': self.comp_allowable_interments(),
                        'loanee_name': self.lot_temp_id[x].partner_id,
                    })
                else:
                    create_blocklots = self.env['stock.production.lot']
                    line_id = create_blocklots.create({
                        'block_number': self.lot_temp_id[x].block_no,
                        'lot_number': self.lot_temp_id[x].lot_no,
                        'name': self.ir_n_name(prod_id, self.lot_temp_id[x].block_no, self.lot_temp_id[x].lot_no)[0],
                        'ref': self.ir_n_name(prod_id, self.lot_temp_id[x].block_no, self.lot_temp_id[x].lot_no)[1],
                        'status': self.lot_temp_id[x].status,
                        'product_id': prod_id.id,
                        'is_new': True,
                        'allowable_interment': self.comp_allowable_interments(),
                        'loanee_name': self.lot_temp_id[x].partner_id,
                    })
                # print self.ir_n_name(prod_id, c, d)
                # 'name': ir_n_name(self.product_id.id)

        return {
            "type": "ir.actions.do_nothing",
        }



class temp_storage(models.TransientModel):
    _name = 'lot.temp'

    stat = [('av', 'Available'),
            ('fp', 'Fully Paid'),
            ('amo', 'Amortized'),
            ('wit', 'Interred'),
            ('fi', 'Fully Interred'),
            ('reserved', 'Reserved'),
            ('ter', 'Terminated')]

    partner_id = fields.Many2one('res.partner', string="Customer")

    lot_gen_id = fields.Many2one('lot.generator')
    block_no = fields.Integer(string="Block")
    lot_no = fields.Integer(string="Lot")
    status = fields.Selection(stat, string="Status", default='av')