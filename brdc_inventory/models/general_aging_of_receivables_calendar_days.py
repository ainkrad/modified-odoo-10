from odoo import api, fields, models
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

class general_aging_of_receivables_calendar_days(models.Model):
    _name = 'general.aging_cd'
    _rec_name = 'so_num'
    _description = 'Aging of Receivables based on Calendar Days'

    invoice_id = fields.Many2one('account.invoice')
    # currency_id = fields.Many2one('res.currency', related='invoice_id.currency_id')
    prod_id = fields.Many2one('product.template', related='invoice_id.invoice_line_ids.product_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)
    so_num = fields.Char(related='invoice_id.origin', string="PA No.")
    partner_name= fields.Char(related='invoice_id.partner_id.name', string="Customer Name")
    date_start = fields.Date(related='invoice_id.date_invoice', string="Date Start")
    contract_price = fields.Monetary(related='invoice_id.amount_total', string="Contract Price")
    principal_payment = fields.Monetary(related='invoice_id.total_principal_payment', string="Payment")
    balance = fields.Monetary(related='invoice_id.residual', string="Balance")
    lpd = fields.Date(related='invoice_id.lpd')

    days_passed = fields.Integer(string="Date Passed", default=0)
    date_today = fields.Date(default=fields.Date.today, string="Date today")
    date_last_paid = fields.Integer(string="Date Last paid", default=0)

    total_due_payment = fields.Monetary(string="Total Due")
    current_due_payment = fields.Monetary(string="Current Due")
    o_to_t = fields.Monetary(string="1-30 Days")
    t_to_s = fields.Monetary(string="31-60 Days")
    s_to_n = fields.Monetary(string="61-90 Days")
    n_a_o = fields.Monetary(string="91 Days Over")

    lpdc = fields.Integer(string="Days Due")

    @api.one
    def get_days_passed(self,dt,pl):
        # return self.env['report'].get_action(self, 'brdc_inventory.general_aging_view')
        # self.date_today = data['form']['aging_date_from']
        # period_length = data['form']['period_length']
        # print self.invoice_id.state

        self.date_today = dt
        period_length = pl

        self.current_due_payment = 0
        self.o_to_t = 0
        self.t_to_s = 0
        self.s_to_n = 0
        self.n_a_o = 0
        due_dp = 0
        due_dp2 = 0
        due_dp3 = 0
        due_dp4 = 0
        cur_dp_due = 0

        j = datetime.strptime(self.date_today, '%Y-%m-%d')
        l = datetime.strptime(self.lpd, '%Y-%m-%d')
        self.lpdc = (j - l).days
        # print self.lpdc
        if self.lpdc >= pl:
            self.lpdc = self.lpdc - pl
        else:
            self.lpdc = 0

        # period_length = 0


        for k in range(1, self.env['invoice.installment.line.dp'].search_count(
                [('account_invoice_id', '=', self.invoice_id.id),
                 ('is_paid', '=', False)]) + 1):
            cur_line = self.env['invoice.installment.line.dp'].search([('account_invoice_id', '=', self.invoice_id.id),
                                                                    ('is_paid', '=', False)])[k - 1]
            e = datetime.strptime(cur_line.date_for_payment, '%Y-%m-%d')
            f = datetime.strptime(self.date_today, '%Y-%m-%d')
            cur_line.days_passed = (f - e).days
            g = cur_line.days_passed

            x = datetime.strptime(self.date_start, '%Y-%m-%d')
            y = datetime.strptime(self.date_today, '%Y-%m-%d')
            self.days_passed = (y-x).days

            x = datetime.strptime(self.date_today, '%Y-%m-%d')
            y = datetime.strptime(self.date_today, '%Y-%m-%d') + relativedelta(months=1)
            period_length = (y-x).days

            if g >= 0 and g <= period_length:
                # print "current due"
                cur_dp_due = cur_line.amount_to_pay
            elif g >= period_length and g <= (period_length * 2):
                # print "due within 30"
                due_dp = cur_line.amount_to_pay
            elif g >= (period_length * 2) and g <= (period_length * 3):
                # print "due within 60"
                due_dp2 = cur_line.amount_to_pay
            elif g >= (period_length * 3) and g <= (period_length * 4):
                # print "due within 90"
                due_dp3 = cur_line.amount_to_pay
            elif g >= (period_length * 4):
                # print "due within 120"
                due_dp4 = cur_line.amount_to_pay

        for i in range(1, self.env['invoice.installment.line'].search_count([('account_invoice_id', '=', self.invoice_id.id),
                                                                               ('is_paid','=',False)])+1):
            cur_line = self.env['invoice.installment.line'].search([('account_invoice_id', '=', self.invoice_id.id),
                                                                               ('is_paid','=',False)])[i-1]
            e = datetime.strptime(cur_line.date_for_payment, '%Y-%m-%d')
            f = datetime.strptime(self.date_today, '%Y-%m-%d')
            cur_line.days_passed = (f - e).days
            g = cur_line.days_passed

            x = datetime.strptime(self.date_start, '%Y-%m-%d')
            y = datetime.strptime(self.date_today, '%Y-%m-%d')
            self.days_passed = (y-x).days

            x = datetime.strptime(self.date_today, '%Y-%m-%d')
            y = datetime.strptime(self.date_today, '%Y-%m-%d') + relativedelta(months=1)
            period_length = (y-x).days

            if g >= 0 and g <= period_length:
                # print "current due"
                self.current_due_payment = cur_line.amount_to_pay
            elif g >= period_length and g <= (period_length * 2):
                # print "due within 30"
                self.o_to_t = cur_line.amount_to_pay
            elif g >= (period_length * 2) and g <= (period_length * 3):
                # print "due within 60"
                self.t_to_s = cur_line.amount_to_pay
            elif g >= (period_length * 3) and g <= (period_length * 4):
                # print "due within 90"
                self.s_to_n = cur_line.amount_to_pay
            elif g >= (period_length * 4):
                # print "due within 120"
                self.n_a_o = cur_line.amount_to_pay

        self.current_due_payment = self.current_due_payment + cur_dp_due
        self.o_to_t = self.o_to_t + due_dp
        self.t_to_s = self.t_to_s + due_dp2
        self.s_to_n = self.s_to_n + due_dp3
        self.n_a_o = self.n_a_o + due_dp4

        self.total_due_payment = self.current_due_payment + self.o_to_t + self.t_to_s + self.s_to_n + self.n_a_o

