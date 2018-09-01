from odoo import api, fields, models


class inherited_product_template(models.Model):
    # _name = 'product.brdc.template' # no name ang old
    _inherit = 'product.template'

    name = fields.Char()

    tracking = fields.Selection(default='serial')
    purchase_ok = fields.Boolean(default=False)

    list_price = fields.Float(default=0.00)

    # area_number = fields.Char(string="Area")
    area_number = fields.Many2one('config.area', string="Area")
    interment_service_type = fields.Many2one('grave_type.list', string="Service Type")

    grave_type = fields.Char(string="Type")
    # no_of_lot = fields.Many2one('oi.no_of_lots', string="Number of Lots", required=True)
    no_of_lot = fields.Integer(default=1, string="Number of Lots", required=True)
    # default=lambda self: self.env['oi.no_of_lots'].search(['name', '=', "1"]))
    dimension = fields.Many2one('oi.dimension', string="Dimension")

    level = fields.Char(string="Level", default='')

    installable_product = fields.Boolean(string="Can be Discounted/Deferred", default=True)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Product already exist"),
    ]

    @api.onchange('categ_id')
    def set_type(self):
        self.grave_type = self.categ_id.name

    # @api.depends('area_number', 'grave_type', 'categ_id','interment_service_type')
    @api.onchange('area_number', 'grave_type', 'categ_id','interment_service_type','level')
    def set_name(self):
        gt = self.grave_type
        if self.area_number.name and gt and self.type != 'service':
            self.name = str(self.area_number.name) + " / " + str(gt)
            if ' ' in str(gt) or '-' in str(gt):
                if '-' in str(gt):
                    st = str(gt).split('-')
                else:
                    st = str(gt).split()
                at = ''
                for t in st:
                    at = at + t[0:1]
                self.default_code =str(self.area_number.name) + at
            else:
                self.default_code =str(self.area_number.name) + str(gt)[0:1]
        elif self.type == 'service':
            self.name =""
            self.no_of_lot = 1
            if self.interment_service_type and self.type:
                self.name = "Interment" + str(gt) + " " + str(self.interment_service_type.name)
                gt = self.interment_service_type.name
                if ' ' in str(gt) or '-' in str(gt):
                    if '-' in str(gt):
                        st = str(gt).split('-')
                    else:
                        st = str(gt).split()
                    at = ''
                    for t in st:
                        at = at + t[0:1]
                if self.grave_type == "Weekends & Holidays":
                    self.default_code = "I" + "WH" + at
                elif self.grave_type == "Weekdays":
                    self.default_code = "I" + "WD" + at
                else:
                    pass
        else:
            self.name = ""
            self.default_code = ""

        if self.grave_type == "Marble Markers":
            self.tracking = 'lot'
            self.sale_ok = False
            self.purchase_ok = True
        else:
            self.tracking = 'serial'
            self.purchase_ok = False
            self.sale_ok = True

        if self.level:
            self.name = self.name + " Level " + self.level
            self.default_code = self.default_code + "L" + self.level[0]

