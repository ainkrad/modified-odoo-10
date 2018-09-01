from odoo import api, fields, models

class inherited_invoice_installment_lines(models.Model):

    _inherit = 'invoice.installment.line'

    days_passed = fields.Integer(string="Days Passed", default=0)