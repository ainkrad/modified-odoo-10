from odoo import api, fields, models

class oi_dimension(models.Model):
    _name = 'oi.dimension'

    _description = 'Dimensions'

    name = fields.Char()

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Product already exist"),
    ]

class oi_no_of_lots(models.Model):
    _name = 'oi.no_of_lots'

    _description = 'Number of Lots'

    name = fields.Char()

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Product already exist"),
    ]

class casket_sizes(models.Model):
    _name = 'oi.casket_sizes'

    _description = 'Casket Sizes'

    name = fields.Char()


class program_language(models.Model):
    _name = 'oi.program_lang'

    _description = 'Program Language'

    name = fields.Char()



