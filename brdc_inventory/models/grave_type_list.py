from odoo import api, fields, models

class grave_type_list(models.Model):
    _name = 'grave_type.list'
    _description = 'List of Grave Types'

    name = fields.Char(string="Types")
