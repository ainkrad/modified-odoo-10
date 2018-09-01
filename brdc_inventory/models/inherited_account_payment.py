from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

# MAP_INVOICE_TYPE_PARTNER_TYPE = {
#     'out_invoice': 'customer',
#     'out_refund': 'customer',
#     'in_invoice': 'supplier',
#     'in_refund': 'supplier',
# }
#
# class inherited_account_payment(models.Model):
#
#     _inherit = 'account.payment'
#
#     @api.model
#     def default_get(self, fields):
#         rec = super(inherited_account_payment, self).default_get(fields)
#         invoice_defaults = self.resolve_2many_commands('invoice_ids', rec.get('invoice_ids'))
#         if invoice_defaults and len(invoice_defaults) == 1:
#             invoice = invoice_defaults[0]
#             rec['communication'] = invoice['reference'] or invoice['name'] or invoice['number']
#             rec['currency_id'] = invoice['currency_id'][0]
#             rec['payment_type'] = invoice['type'] in ('out_invoice', 'in_refund') and 'inbound' or 'outbound'
#             rec['partner_type'] = MAP_INVOICE_TYPE_PARTNER_TYPE[invoice['type']]
#             rec['partner_id'] = invoice['partner_id'][0]
#             # rec['amount'] = invoice['residual']
#             rec['amount'] = 0.00
#         return rec
#
#     @api.multi
#     def post(self):
#         """ Create the journal items for the payment and update the payment's state to 'posted'.
#             A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
#             and another in the destination reconciliable account (see _compute_destination_account_id).
#             If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
#             If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
#         """
#         # block_serial = self.env['invoice.installment.line']
#         # block_serial.search([('product_id', '=', self.product_id.id), ('inventory_id', '=', self.id)]).unlink()
#
#         inv_line_dp = self.env['invoice.installment.line.dp'].search(
#             [('account_invoice_id', '=', self.env['account.invoice'].search([('number', '=', self.communication)]).id),
#              ('is_paid', '=', False)])
#         inv_line = self.env['invoice.installment.line'].search(
#             [('account_invoice_id', '=', self.env['account.invoice'].search([('number', '=', self.communication)]).id),
#              ('is_paid', '=', False)])
#
#         if len(inv_line_dp) >= 1:
#             if inv_line_dp[0].amount_to_pay < self.amount:
#                 inv_line_dp[0].notes = self.name
#                 inv_line_dp[0].is_paid = True
#             else:
#                 raise ValidationError(_("Payment Amount less than Balance"))
#         elif len(inv_line_dp) <= 0:
#             if inv_line[0].amount_to_pay < self.amount:
#                 inv_line[0].notes = self.name
#                 inv_line[0].is_paid = True
#                 inv_line[1].amount_to_pay = self.amount - inv_line[1].amount_to_pay
#             else:
#                 raise ValidationError(_("Payment Amount less than Balance"))
#                 # print self.amount
#                 # print inv_line[0].amount_to_pay
#
#
#         for rec in self:
#
#             if rec.state != 'draft':
#                 raise UserError(
#                     _("Only a draft payment can be posted. Trying to post a payment in state %s.") % rec.state)
#
#             if any(inv.state != 'open' for inv in rec.invoice_ids):
#                 raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))
#
#             # Use the right sequence to set the name
#             if rec.payment_type == 'transfer':
#                 sequence_code = 'account.payment.transfer'
#             else:
#                 if rec.partner_type == 'customer':
#                     if rec.payment_type == 'inbound':
#                         sequence_code = 'account.payment.customer.invoice'
#                     if rec.payment_type == 'outbound':
#                         sequence_code = 'account.payment.customer.refund'
#                 if rec.partner_type == 'supplier':
#                     if rec.payment_type == 'inbound':
#                         sequence_code = 'account.payment.supplier.refund'
#                     if rec.payment_type == 'outbound':
#                         sequence_code = 'account.payment.supplier.invoice'
#             rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(
#                 sequence_code)
#             if not rec.name and rec.payment_type != 'transfer':
#                 raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))
#
#             # Create the journal entry
#             amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
#             move = rec._create_payment_entry(amount)
#
#             # In case of a transfer, the first journal entry created debited the source liquidity account and credited
#             # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
#             if rec.payment_type == 'transfer':
#                 transfer_credit_aml = move.line_ids.filtered(
#                     lambda r: r.account_id == rec.company_id.transfer_account_id)
#                 transfer_debit_aml = rec._create_transfer_entry(amount)
#                 (transfer_credit_aml + transfer_debit_aml).reconcile()
#
#             rec.write({'state': 'posted', 'move_name': move.name})



class inherited_account_invoice(models.Model):

    _inherit = 'account.invoice'

    agent_id = fields.Many2one('res.partner', related="sale_order_id.agent_id")
    # name = fields.Char()
    def rend(self):
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'brdc_inventory.customer_ledger_view',
            'context': self.env.context['active_id'],
        }

    def print_ledger(self):
        return self.rend()


class inherited_account_invoice_line(models.Model):

    _inherit = 'account.invoice.line'

    lot_id = fields.Many2one('stock.production.lot', string="Lot / Vault")

    # lot_id = fields.Char(string="Lot / Vault") here doggy
