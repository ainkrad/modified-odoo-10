from odoo import api, fields, models

class config_area(models.Model):
    _name = 'config.area'
    _rec_name = 'name'
    _description = 'List of Area'

    name = fields.Char()

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Area already exist"),
    ]

class config_dimension(models.Model):
    _name = 'config.dimension'
    _rec_name = 'name'
    _description = 'List of Dimensions'
    name = fields.Char()

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Product already exist"),
    ]