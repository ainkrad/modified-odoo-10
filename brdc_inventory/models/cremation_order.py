from odoo import api, fields, models, _
from odoo.exceptions import UserError

class cremation_order(models.Model):
    _name = 'cremation.order'
    # _rec_name = 'name'
    _description = 'Cremation Order'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    # name = fields.Char(string="CO No.", default=)
    or_id = fields.Many2one('sale.order', string="Ref No.")
    deceased_id = fields.One2many('deceased.list', 'interment_id')

    cremation_date = fields.Date(string="Scheduled Date")
    date_cremated = fields.Date(string="Date Cremated")

    release_type = fields.Selection(string="Release type", selection=[('takeout', 'Bring home'), ('dinein', 'In house'), ], required=False, )
    informant_id = fields.Many2one('res.partner', string="Name of Informant")

    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'
        return {
            "type": "ir.actions.do_nothing",
        }

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'
        self.or_id.is_used = True
        if len(self.deceased_id) <= 0:
            return {
                'warning': {
                    'title': "Error",
                    'message': "Please set deceased to be interred",
                },
            }
        return {
            "type": "ir.actions.do_nothing",
        }

    @api.multi
    def action_done(self):
        self.state = 'done'

        if len(self.deceased_id) >= 1:
            for c in (0, len(self.deceased_id) - 1):
                self.deceased_id[c].departed_id.is_deceased = True
        return {
            "type": "ir.actions.do_nothing",
        }

    @api.multi
    def unlink(self):
        for quo in self:
            if quo.state != 'draft':
                raise UserError(_("Cannot delete confirmed application"))
            return super(cremation_order, self).unlink()
