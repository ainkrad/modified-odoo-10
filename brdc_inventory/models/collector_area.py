from odoo import api, fields, models

class collector_area(models.Model):
    _name = 'collector.area'
    _rec_name = 'name'
    _description = 'Collector Area'

    name = fields.Char(string="Area")

    barangay_id = fields.Many2many('config.barangay', string="List of Baranggay")

    partner_id = fields.Many2many('res.partner', string="List of Collector Assigned")