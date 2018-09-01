from odoo import api, fields, models

class assume_invoices(models.Model):
    _name = 'assume.invoices'
    # _rec_name = 'name'
    _description = 'Assume transaction records'


    new_partner_id = fields.Many2one('res.partner', string="Assignee")
    old_partner_id = fields.Many2one('res.partner')