from odoo import api, fields, models
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

class customer_aging_of_receivables(models.Model):
    _name = 'general.aging'
    _rec_name = 'so_num'
    _description = 'List of Customer Aging of Receivables'

    invoice_id = fields.Many2one('account.invoice')
    # currency_id = fields.Many2one('res.currency', related='invoice_id.currency_id')
    prod_id = fields.Many2one('product.template', related='invoice_id.invoice_line_ids.product_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id, store=True)
    so_num = fields.Char(related='invoice_id.origin', string="PA No.", store=True)
    pa_ref = fields.Char(related='invoice_id.pa_ref')
    partner_name= fields.Char(related='invoice_id.partner_id.name', string="Customer Name", store=True)
    date_start = fields.Date(related='invoice_id.date_invoice', string="Date Start")
    contract_price = fields.Monetary(related='invoice_id.amount_total', string="Contract Price", store=True)
    principal_payment = fields.Monetary(related='invoice_id.total_principal_payment', string="Payment", store=True)
    balance = fields.Monetary(related='invoice_id.residual', string="Balance", store=True)
    lpd = fields.Date(related='invoice_id.lpd')

    days_passed = fields.Integer(string="Date Passed", default=0)
    date_today = fields.Date(default=fields.Date.today, string="Date today")
    date_last_paid = fields.Integer(string="Date Last paid", default=0)

    total_due_payment = fields.Monetary(string="Total Due", store=True)
    current_due_payment = fields.Monetary(string="Current Due", store=True)
    o_to_t = fields.Monetary(string="1-30 Days", store=True)
    t_to_s = fields.Monetary(string="31-60 Days", store=True)
    s_to_n = fields.Monetary(string="61-90 Days", store=True)
    n_a_o = fields.Monetary(string="91 Days Over", store=True)

    lpdc = fields.Integer(string="Days Due", store=True)

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

            if g >= 0 and g <= 30:
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

            if g >= 0 and g <= 30:
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

        # print self.env['invoice.installment.line'].search([('account_invoice_id', '=', self.invoice_id.id),('is_paid','=',False)])

        # for c in self.invoice_id:
        #     for k in range(1, self.env['invoice.installment.line'].search_count(
        #             [('account_invoice_id', '=', self.invoice_id.id),
        #              ('is_paid', '=', False)]) + 1):
        #         # print self.env['invoice.installment.line'].search([('account_invoice_id', '=', self.invoice_id.id),('is_paid','=',False)])[k - 1].date_for_payment
        #
        #         cur_line = self.env['invoice.installment.line'].search([('account_invoice_id', '=', self.invoice_id.id),
        #                                                                 ('is_paid', '=', False)])[k - 1]
        #         z = datetime.strptime(cur_line.date_for_payment, '%Y-%m-%d')
        #         x = datetime.strptime(self.date_today, '%Y-%m-%d')
        #         y = timedelta(days = 30)
        #         if (x - (y * 3) <= z <= x + (y * 3)) and cur_line.is_paid is False:
        #             print "Due within 90 days:" + cur_line.date_for_payment
        #         elif (x - (y * 2) <= z <= x + (y * 2)) and cur_line.is_paid is False:
        #             print "Due within 60 days:" + cur_line.date_for_payment
        #         elif (x - y <= z <= x + y) and cur_line.is_paid == False:
        #             print "Due within 30 days:" + cur_line.date_for_payment
        #         else:
        #             print False

            #somehow working

            # self.current_due_payment = 0
            # self.o_to_t = 0
            # self.t_to_s = 0
            # self.s_to_n = 0
            # self.n_a_o = 0
            # due_dp = 0
            # due_dp2 = 0
            # due_dp3 = 0
            # due_dp4 = 0
            # cur_dp_due = 0

            # for k in range(1, self.env['invoice.installment.line.dp'].search_count(
            #         [('account_invoice_id', '=', self.invoice_id.id),
            #          ('is_paid', '=', False)]) + 1):
            #     cur_line = self.env['invoice.installment.line.dp'].search([('account_invoice_id', '=', self.invoice_id.id),
            #                                                             ('is_paid', '=', False)])[k - 1]
            #     x = datetime.strptime(cur_line.date_for_payment, '%Y-%m-%d')
            #     y = datetime.strptime(self.date_today, '%Y-%m-%d')
            #     g = (y - x).days + 30
            #
            #     e = datetime.strptime(self.date_start, '%Y-%m-%d')
            #     f = datetime.strptime(self.date_today, '%Y-%m-%d')
            #     self.days_passed = (f - e).days
            #
            #     if g >= 0 and g <= 29:
            #         print "current due"
            #         # cur_dp_due = cur_line.amount_to_pay
            #     elif g >= 30 and g <= 60:
            #         print "due within 30"
            #         # due_dp = cur_line.amount_to_pay
            #     elif g >= 60 and g <= 90:
            #         print "due within 60"
            #         # due_dp2 = cur_line.amount_to_pay
            #     elif g >= 90 and g <= 120:
            #         print "due within 90"
            #         # due_dp3 = cur_line.amount_to_pay
            #     elif g >= 120:
            #         print "due within 120"
            #         # due_dp4 = cur_line.amount_to_pay
        #
            # for i in range(1, self.env['invoice.installment.line'].search_count([('account_invoice_id', '=', self.invoice_id.id),
            #                                                                        ('is_paid','=',False)])+1):
            #     cur_line = self.env['invoice.installment.line'].search([('account_invoice_id', '=', self.invoice_id.id),
            #                                                                        ('is_paid','=',False)])[i-1]
            #     x = datetime.strptime(cur_line.date_for_payment, '%Y-%m-%d')
            #     y = datetime.strptime(self.date_today, '%Y-%m-%d')
            #     g = (y-x).days + 30
            #
            #     e = datetime.strptime(self.date_start, '%Y-%m-%d')
            #     f = datetime.strptime(self.date_today, '%Y-%m-%d')
            #     self.days_passed = (f-e).days
            #
            #     print cur_line.date_for_payment, g, self.days_passed
            #
            #     if g >= 0 and g <= 29:
            #         # print "current due"
            #         self.current_due_payment = cur_line.amount_to_pay
            #     elif g >= 30 and g <= 60:
            #         # print "due within 30"
            #         self.o_to_t = cur_line.amount_to_pay
            #     elif g >= 60 and g <= 90:
            #         # print "due within 60"
            #         self.t_to_s = cur_line.amount_to_pay
            #     elif g >= 90 and g <= 120:
            #         # print "due within 90"
            #         self.s_to_n = cur_line.amount_to_pay
            #     elif g >= 120:
            #         # print "due within 120"
            #         self.n_a_o = cur_line.amount_to_pay
            #
            #     self.current_due_payment = self.current_due_payment + cur_dp_due
            #     self.o_to_t = self.o_to_t + due_dp
            #     self.t_to_s = self.t_to_s + due_dp2
            #     self.s_to_n = self.s_to_n + due_dp3
            #     self.n_a_o = self.n_a_o + due_dp4
            #
            #     self.total_due_payment = self.current_due_payment + self.o_to_t + self.t_to_s + self.s_to_n + self.n_a_o

                #somehow working

            # for i in range(1, len(self.invoice_id.InvoiceInstallmentLine_ids)+1):
            #     # self.days_passed = 0
            #     cur_line = self.invoice_id.InvoiceInstallmentLine_ids[i-1]
            #     x = datetime.strptime(cur_line.date_for_payment, '%Y-%m-%d')
            #     y = datetime.strptime(self.date_start, '%Y-%m-%d')
            #     g = abs((y-x).days)
            #
            #     e = datetime.strptime(self.date_start, '%Y-%m-%d')
            #     f = datetime.strptime(self.date_today, '%Y-%m-%d')
            #     self.days_passed = abs((f-e).days)
            #
            #     print g, self.days_passed, cur_line.date_for_payment, cur_line.amount_to_pay, cur_line.is_paid

                # # plus 20 lang man na diba ano gid ang kabudlay dira Ian haw? -.-
                # if self.days_passed <= 30 and self.days_passed >= 1 and cur_line.is_paid == False:
                #     self.current_due_payment = cur_line.amount_to_pay
                # elif self.days_passed <= 30 and self.days_passed >= 1 and cur_line.is_paid == True:
                #     self.current_due_payment = 0
                # if self.days_passed > 30 and self.days_passed < 60 and self.current_due_payment != 0 and cur_line.is_paid == False:
                #     self.o_to_t = cur_line.amount_to_pay
                # elif self.days_passed > 30 and self.days_passed < 60 and self.current_due_payment != 0 and cur_line.is_paid == True:
                #     self.o_to_t = 0
                # if self.days_passed > 60 and self.days_passed < 90 and self.o_to_t != 0 and cur_line.is_paid == False:
                #     self.t_to_s = cur_line.amount_to_pay
                # elif self.days_passed > 60 and self.days_passed < 90 and self.o_to_t != 0 and cur_line.is_paid == True:
                #     self.t_to_s = 0
                # if self.days_passed > 90 and self.days_passed < 120 and self.t_to_s != 0 and cur_line.is_paid == False:
                #     self.s_to_n = cur_line.amount_to_pay
                # elif self.days_passed > 90 and self.days_passed < 120 and self.t_to_s != 0 and cur_line.is_paid == True:
                #     self.s_to_n = 0
                # if self.days_passed > 120 and self.s_to_n != 0 and cur_line.is_paid == False:
                #     self.n_a_o = cur_line.amount_to_pay
                # elif self.days_passed > 120 and self.s_to_n != 0 and cur_line.is_paid == True:
                #     self.n_a_o = 0


                # elif self.days_passed >= g:

                # if g > 90 and self.days_passed > 90:
                #     self.n_a_o = cur_line.amount_to_pay
                # elif g > 60 and g < 90 and self.days_passed > 60 and self.days_passed < 90:
                #     self.s_to_n = cur_line.amount_to_pay
                # elif g > 30 and g < 60 and self.days_passed > 30 and self.days_passed < 60:
                #     self.t_to_s = cur_line.amount_to_pay
                # elif g <=30:
                #     self.o_to_t = cur_line.amount_to_pay
                # else:
                #     self.o_to_t = 0
                #     self.t_to_s = 0
                #     self.s_to_n = 0
                #     self.n_a_o = 0


            # print self.date_today
            # self.o_to_t = 0
            # self.t_to_s = 0
            # self.s_to_n = 0
            # self.n_a_o = 0
            # self.current_due_payment = 0
            # due_dp = 0
            # due_dp2 = 0
            # due_dp3 = 0
            # due_dp4 = 0
            # cur_dp_due = 0

            # for i in range(0, len(self.invoice_id.InvoiceInstallmentLineDP_ids)+1):
            #     self.days_passed = 0
            #     cur_line = self.invoice_id.InvoiceInstallmentLineDP_ids[i-1]
            #     x = datetime.strptime(cur_line.date_for_payment, '%Y-%m-%d')
            #     y = datetime.strptime(self.date_today, '%Y-%m-%d')
            #     self.days_passed = abs((y-x).days)
            #     # print self.days_passed
            #     if self.days_passed >- 1 and self.days_passed <= 30 and cur_line.is_paid == False:
            #         cur_dp_due = cur_line.amount_to_pay
            #     if self.days_passed >= 31 and self.days_passed <= 60 and cur_line.is_paid == False:
            #         due_dp = cur_line.amount_to_pay
            #     if self.days_passed >= 61 and self.days_passed <= 90 and cur_line.is_paid == False:
            #         due_dp2 = cur_line.amount_to_pay
            #     if self.days_passed >= 91 and self.days_passed <= 120 and cur_line.is_paid == False:
            #         due_dp3 = cur_line.amount_to_pay
            #     if self.days_passed >= 121 and cur_line.is_paid == False:
            #         due_dp4 = cur_line.amount_to_pay

            # cur_line = 0
            #
            # for i in range(0, len(self.invoice_id.InvoiceInstallmentLine_ids)+1):
            #     self.days_passed = 0
            #     cur_line = self.invoice_id.InvoiceInstallmentLine_ids[i-1]
            #     x = datetime.strptime(cur_line.date_for_payment, '%Y-%m-%d')
            #     y = datetime.strptime(self.date_today, '%Y-%m-%d')
            #     g = abs((y-x).days)
            #
            #     e = datetime.strptime(self.date_start, '%Y-%m-%d')
            #     f = datetime.strptime(self.date_today, '%Y-%m-%d')
            #     self.days_passed = abs((f-e).days)
            #
            #     if g >= self.days_passed and self.days_passed >= 1 and self.days_passed <= 30 and cur_line.is_paid == False:
            #         self.current_due_payment = cur_line.amount_to_pay
            #     elif g >= self.days_passed and self.days_passed >= 31 and self.days_passed <= 60 and cur_line.is_paid == False:
            #         self.o_to_t = self.current_due_payment
            #     elif g >= self.days_passed and self.days_passed >= 61 and self.days_passed <= 90 and cur_line.is_paid == False:
            #         self.t_to_s = self.current_due_payment
            #     elif g >= self.days_passed and self.days_passed >= 91 and self.days_passed <= 120 and cur_line.is_paid == False:
            #         self.s_to_n = self.current_due_payment
            #     elif g >= self.days_passed and self.days_passed >= 121 and cur_line.is_paid == False:
            #         self.s_to_n = self.current_due_payment

                # print self.days_passed
                # if self.days_passed >- 1 and self.days_passed <= 31 and cur_line.is_paid == False and self.days_passed >= g:
                #     self.n_a_o = cur_line.amount_to_pay + due_dp4
                # if self.days_passed >= 30 and self.days_passed <= 60 and cur_line.is_paid == False and self.days_passed >= g:
                #     self.s_to_n = cur_line.amount_to_pay + due_dp3
                # if self.days_passed >= 61 and self.days_passed <= 90 and cur_line.is_paid == False and self.days_passed >= g:
                #     self.t_to_s = cur_line.amount_to_pay + due_dp2
                # if self.days_passed >= 91 and self.days_passed <= 120 and cur_line.is_paid == False and self.days_passed >= g:
                #     self.o_to_t = cur_line.amount_to_pay + due_dp
                # if self.days_passed >= 121 and cur_line.is_paid == False:
                #     self.current_due_payment = cur_line.amount_to_pay + cur_dp_due

            # self.total_due_payment = self.current_due_payment + self.o_to_t + self.t_to_s + self.s_to_n + self.n_a_o

                # if self.days_passed > - 1 and self.days_passed <= 31 and cur_line.is_paid == False:
                #     self.current_due_payment = cur_line.amount_to_pay + cur_dp_due
                # elif self.days_passed >= 30 and self.days_passed <= 60 and cur_line.is_paid == False:
                #     self.o_to_t = self.current_due_payment + due_dp
                # elif self.days_passed >= 61 and self.days_passed <= 90 and cur_line.is_paid == False:
                #     self.t_to_s = self.o_to_t + due_dp2
                # elif self.days_passed >= 91 and self.days_passed <= 120 and cur_line.is_paid == False:
                #     self.s_to_n = self.t_to_s + due_dp3
                # elif self.days_passed >= 121 and cur_line.is_paid == False:
                #     self.n_a_o = self.s_to_n + due_dp4




