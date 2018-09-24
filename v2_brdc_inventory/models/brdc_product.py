from odoo import api, fields, models

class brdc_product(models.Model):
    _name = 'brdc.product'
    # _rec_name = 'name'
    # _description = 'BRDC Products'
    _inherits = {'product.template': 'brdc_prd_tmpl'}
    # name = fields.Char()

    brdc_prd_tmpl = fields.Many2one('product.template','BRDC Product')

    area_name = fields.Many2one('config.area', string="Area")
    dimension = fields.Many2one('config.dimension', string="Dimension")
    level = fields.Char(string="Level", default='')
    no_of_lot = fields.Integer(default=1, string="Number of Lots", required=True)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Product already exist"),
    ]