from odoo.exceptions import ValidationError

from odoo import api, fields, models

import time, datetime


class sold_product_per(models.TransientModel):
    _name = 'sold.lots'
    _rec_name = 'name'
    _description = 'Sold Lots per Day, Month and Year'

    name = fields.Char()

    sold_product_filter = fields.Selection(string="Generate per", selection=[('day', 'Day'), ('month', 'Month'), ('year', 'Year')], required=False, )

    product_id = fields.Many2one('product.template', string="Product")

    # per_day = fields.Date(string="Day of", default=lambda *a: time.strftime('%Y-%m-%d'))
    from_date = fields.Date(string="From", default=lambda *a: time.strftime('%Y-%m-%d'))
    to_date = fields.Date(string="To", default=lambda *a: time.strftime('%Y-%m-%d'))

    @api.multi
    def print_sold_lot_per_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['sold_product_filter', 'product_id', 'from_date','to_date'])[0]
        # print data
        # aging_date_from =generate_general_aging data['form']['aging_date_from']
        # period_length = data['form']['period_length']
        # print aging_date_from, period_length
        sale_order = self.env['sale.order'].search([])
        prod_id = data['form']['product_id']
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
        # print sale_order, prod_id, per_day
        return self._print_report(data)

    def _print_report(self, data):
        # print 'test handler'
        # data['form'].update(self.read(['aging_date_from', 'period_length'])[0])
        # data = {}
        # data['form'] = self.read(['course_id', 'batch_id'])[0]
        return self.env['report'].get_action(self, 'brdc_inventory.sold_lots_per_view', data=data)
    pass

class sold_lot_per_render(models.AbstractModel):
    _name = 'report.brdc_inventory.sold_lots_per_view'

    _description = 'Sold Lots'

    @api.multi
    def render_html(self, docids, data):
        print "pumasok ako"

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))

        # print data
        # ps = data['form']['prod_sel'][0]
        # fp = data['form']['filter_per']
        # print fp, ps
        #
        # if fp == 'prod' and ps:
        #     recs = self.env['general.aging'].search([('prod_id','=',ps)])
        # else:
        # if data['form']['filter_per'] == 'prod':
        #     ps = data['form']['prod_sel'][0]
        #     recs = self.env['general.aging'].search([('prod_id','like',ps), ('balance','!=',0), ('total_due_payment','!=',0)])
        # elif data['form']['filter_per'] == 'gen':
        #     recs = self.env['general.aging'].search([('balance','!=',0), ('total_due_payment','!=',0)])
        # elif data['form']['filter_per'] == 'area':
        #     # print data['form']['area_list']
        #     # for c in range(0,len(data['form']['area_list'])):
        #     recs = self.env['general.aging'].search([('balance', '!=', 0), ('total_due_payment', '!=', 0),
        #                                              ('invoice_id.partner_id.barangay_id.id', 'in', data['form']['area_list'])])
        # if data['form']['sold_product_filter'] == 'day':
            # ('prod_id', '=', data['form']['prod_id']),
            # print data['form']['product_id'][0]

        ddf = data['form']['from_date']
        ddt = data['form']['to_date']
        recs = self.env['sale.order'].search([('prod_id','=',data['form']['product_id'][0])
                                                              ,('date_for_payment','<=',ddt),('date_for_payment','>=',ddf)
                                             ,('is_interment', '!=', 'TRUE'),('is_crematory', '!=', 'TRUE')])
        print recs
        # fp = data['form']['filter_per']
        # print fp
        if len(recs) >= 0:
            recs
        else:
            raise ValidationError("No Record Found!")


        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'recs': recs,
            # 'notiftypecount': notiftypecount,
        }

        return self.env['report'].render('brdc_inventory.sold_lots_per_view', docargs)
