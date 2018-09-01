from odoo import api, fields, models

class employee_hierarchy(models.Model):
    _name = 'employee.hierarchy'
    # _rec_name = 'name'
    _description = 'Employee Hierarchy'

    name = fields.Char(string="Position")
    comm_percent = fields.Float(string="Commission Percentage")