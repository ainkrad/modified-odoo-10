from odoo import api, fields, models

class inherited_sale_advance_payment_inv(models.TransientModel):

    _inherit = 'sale.advance.payment.inv'

    advance_payment_method = fields.Selection(default='delivered')
