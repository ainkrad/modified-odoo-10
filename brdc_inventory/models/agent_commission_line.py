from odoo import api, fields, models

class agent_commission_line(models.Model):
    _name = 'agent.commission.line'
    _rec_name = 'name'
    _description = 'List of all commissions given to SA, AM, UM'

    name = fields.Char()
    sa_percentage = fields.Float(default=0,string="Sales Agent Commission")
    am_percentage = fields.Float(default=0,string="Agency Manager Commission")
    um_percentage = fields.Float(default=0,string="Unit Manager Commission")
    employee_commission_id = fields.Many2one('employee.commission','agent_commission_line')

    is_distributed = fields.Boolean(default=False,string="Is Distributed")
    date_distributed = fields.Date(string="Date distributed")

    invoice_id = fields.Many2one('account.payment', string="Reference Payment")
    is_paid = fields.Boolean(string="Is Paid", default=False)
    date_paid = fields.Date(string="Date Paid")