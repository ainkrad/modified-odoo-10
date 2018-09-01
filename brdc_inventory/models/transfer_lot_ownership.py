from odoo import api, fields, models
import time

class transfer_lot_ownership(models.Model):
    _name = 'transfer.owner'
    # _rec_name = 'name'
    _description = 'Transferred ownership'

    # name = fields.Char()

    lot_id = fields.Many2one('stock.production.lot')
    transfer_from = fields.Many2one('res.partner')
    transfer_to = fields.Many2one('res.partner')
    date_transferred = fields.Date(default=lambda *a: time.strftime('%Y-%m-%d'), readonly=True)

    #payment proof