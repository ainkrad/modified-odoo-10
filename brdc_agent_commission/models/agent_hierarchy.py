from odoo import api, fields, models

class agent_hierarchy(models.Model):
    _name = 'agent.hierarchy'
    # _rec_name = 'name'
    _description = 'Agent Hierarchy'

    name = fields.Char(string="Position")
    comm_percent = fields.Float(string="Commission Percentage")

    agent_list = fields.One2many('res.partner','agency_id')