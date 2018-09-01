from odoo import api, fields, models


class inherited_product_product(models.Model):
    # _name = 'product.brdc.product'
    _inherit = 'product.product'

    # name = fields.Char()

    # tracking = fields.Selection(default='serial')
    # purchase_ok = fields.Boolean(default=False)

    # list_price = fields.Float(default=0.00)

    # area_number = fields.Char(string="Area")
    # grave_type = fields.Char(string="Type")

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Product already exist"),
    ]

    @api.onchange('categ_id')
    def set_type(self):
        self.grave_type = self.categ_id.name
        if self.grave_type == "Marble Markers":
            self.tracking = 'lot'
            self.sale_ok = False
            self.purchase_ok = True

        else:
            self.tracking = 'serial'
            self.purchase_ok = False
            self.sale_ok = True

    @api.depends('area_number', 'grave_type', 'categ_id')
    @api.onchange('area_number', 'grave_type', 'categ_id')
    def set_name(self):
        gt = self.grave_type
        if self.area_number.name and gt:
            self.name = "Area " + str(self.area_number.name) + " / " + str(gt)
            if ' ' in str(gt) or '-' in str(gt):
                if '-' in str(gt):
                    st = str(gt).split('-')
                else:
                    st = str(gt).split()
                at = ''
                for t in st:
                    at = at + t[0:1]
                self.default_code = "A" + str(self.area_number.name) + at
            else:
                self.default_code = "A" + str(self.area_number.name) + str(gt)[0:1]
        else:
            # self.name = ""
            self.default_code = ""

