from odoo import api, fields, models

class config_area(models.Model):

    _name = 'config.area'
    _description = 'Area numbers'

    name = fields.Char(string="Area")

    # num_of_blocks = fields.Integer(string="Number of Blocks per Area", default=0)
    # num_of_lots = fields.Integer(string="Number of Lots per Block", default=0)
    #
    # block_line_ids = fields.One2many('block.serial', 'area_id')
    #
    # # @api.onchange('num_of_blocks')
    # def set_blocks(self):
    #     block_serial = self.env['block.serial']
    #     block_serial.search([('area_id', '=', self.id)]).unlink()
    #
    #     for c in range(1,self.num_of_blocks+1):
    #         line_id = block_serial.create({
    #             'area_id': self.id,
    #             'block_number': c,
    #             'lot_number': self.num_of_lots
    #         })

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The Area already exist"),
    ]


# class block_serial(models.Model):
#     _name = 'block.serial'
#
#     _description = 'Block and Serials'
#
#     # name = fields.Char()
#
#     area_id = fields.Many2one('config.area', string="Area id")
#     block_number = fields.Integer(string="Block")
#     lot_number = fields.Integer(string="Lot")
