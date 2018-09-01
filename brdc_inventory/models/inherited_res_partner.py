from odoo import api, fields, models

class inherited_res_partner(models.Model):

    _inherit = 'res.partner'

    # agency_id = fields.Many2one('employee.hierarchy')

    # Ranz
    collector_area_id = fields.Many2many('config.barangay', string="Barangay assigned")
    # Ranz

