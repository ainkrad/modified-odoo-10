from odoo import api, fields, models, _
from odoo.exceptions import UserError

class interment_order(models.Model):
    _name = 'interment.order2'
    _rec_name = 'or_id'
    _description = 'Interment Orders'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    or_id = fields.Many2one('sale.order', string="Ref No.")
    inter_type = fields.Selection(string="Interment Type", selection=[('inter', 'Interment'), ('bt', 'Bone Transfer'), ])
    # nature_of_interment = fields.Selection(string="Nature of Interment", selection=[('fres', 'Fresh'), ('bon', 'Bone'), ], required=False, )

    deceased_id = fields.One2many('deceased.list', 'interment_id')
    deceased = fields.Char(store=False, related='deceased_id.departed_id.name')
    d_of_d = fields.Date(store=False, related='deceased_id.date_of_death')
    c_of_d = fields.Text(store=False, related='deceased_id.cause_of_death')

    fname = fields.Char(string="First Name", related='deceased_id.departed_id.first_name')
    mname = fields.Char(string="Middle Name", related='deceased_id.departed_id.middle_name')
    lname = fields.Char(string="Last Name", related='deceased_id.departed_id.last_name')
    d_of_b = fields.Date(store=False, related='deceased_id.date_of_birth')
    # departed_id = fields.Many2one('res.partner', string="Name of Departed", required=True)
    # date_of_birth = fields.Date(string="Date of Birth", related='departed_id.birthdate', store=False)
    # date_of_death = fields.Date(string="Date of Death")
    # cause_of_death = fields.Text(string="Cause of Death")
    # religion = fields.Char(string="Religion", related='departed_id.religion_id.name', store=False)

    informant_id = fields.Many2one('res.partner', string="Name of Informant", required=True)
    relationship_departed = fields.Char(string="Relationship with the Departed")
    # Address
    fb_account = fields.Char(string="FB Account")
    contact_number = fields.Char(string="Contact Number", related='informant_id.phone', store=False)

    song_ids = fields.One2many(comodel_name="song.request", inverse_name="interment_order_id", string="Requested Songs", required=False, limit=4)
    message = fields.Text(string="Message")

    casket_size = fields.Many2one('oi.casket_sizes', string="Casket Size")
    wake_address = fields.Text(string="Wake Address")

    product_id = fields.Many2one('product.product',string='Product and Class', related='or_id.prod_id', required=True)

    lot_id = fields.Many2one('stock.production.lot', string='Lot / Vault', related='or_id.lot_id', required=True)


    # product_id = fields.Many2one('product.product',string='Product and Class',
    #                              # default=_get_pricelist_item,
    #                              domain=[('type', 'in', ['consu','product']), ('sale_ok', '=', 'True')],
    #                              required=True)
    #
    # lot_id = fields.Many2one('stock.production.lot', string='Lot / Vault', required=True)

    # lot_owner = fields.Char(string="Lot Owner", related='lot_id.loanee_name', store=False)#Important

    interment_td = fields.Datetime(string="Date and Time", required=True)
    interment_lang = fields.Many2one('oi.program_lang', string="Program Language")

    mass_td = fields.Datetime(string="Date and Time", required=True)
    mass_loc = fields.Text(string="Location")

    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ], default='draft')

    @api.onchange('interment_td')
    def set_td(self):
        if self.interment_td:
            self.mass_td = self.interment_td
        return {
            "type": "ir.actions.do_nothing",
        }


    @api.multi
    def action_draft(self):
        self.state = 'draft'
        # self.lot_id.status = 'av'
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
        if self.product_id.grave_type == "Community Vault":
            max_int = int(self.product_id.no_of_lot)
        else:
            max_int = int(self.product_id.no_of_lot) * 2

        if self.env['interment.order2'].search_count([('lot_id', '=', self.lot_id.id)]) >= max_int:
            self.lot_id.status = 'fi'
        else:
            self.lot_id.status = 'wit'

        if len(self.deceased_id) >= 1:
            for c in (0, len(self.deceased_id)-1):
                self.deceased_id[c].departed_id.is_deceased = True
        return {
            "type": "ir.actions.do_nothing",
        }

    @api.multi
    def unlink(self):
        for quo in self:
            if quo.state != 'draft':
                raise UserError(_("Cannot delete confirmed application"))
            return super(interment_order, self).unlink()

    # @api.constrains('age')
    # def _check_something(self):
    #     for record in self:
    #         if record.age > 20:
    #             raise ValidationError("Your record is too old: %s" % record.age)
    #     # all records passed the test, don't return anything


class SongRequest(models.Model):
    _name = 'song.request'

    name = fields.Char(required=1, string='Requested Song')
    interment_order_id = fields.Many2one('interment.order', string='Interment Order')