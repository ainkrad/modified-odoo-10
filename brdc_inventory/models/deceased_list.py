from odoo import api, fields, models

class deceased_list(models.Model):
    _name = 'deceased.list'
    _rec_name = 'departed_id'
    _description = 'List of all Deceased'

    interment_id = fields.Many2one('interment.order2','deceased_id')
    departed_id = fields.Many2one('res.partner',string="Deceased")
    date_of_death = fields.Date(string="Date of Death")
    cause_of_death = fields.Text(string="Cause of Death")
    date_of_birth = fields.Date(string="Date of Birth", related='departed_id.birthdate')
    religion = fields.Char(string="Religion", related='departed_id.religion_id.name', store=False)
    n_of_interment = fields.Selection(string="Nature of Interment", selection=[('fres', 'Fresh'), ('bon', 'Bone'), ])































    # print "i love myself and i and u. me and you if me is equal to handsome, then me is false. Thank you and Mabuhay!"
    # Saranghae i love korean actors