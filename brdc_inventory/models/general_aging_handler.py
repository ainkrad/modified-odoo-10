from odoo import api, fields, models
from datetime import datetime, timedelta
import time

class general_aging_handler(models.TransientModel):
    _name = 'general.aging_handler'
    # _rec_name = 'name'
    _description = 'General Aging handler'

    aging_date_from = fields.Date(string="As of", default=lambda *a: time.strftime('%Y-%m-%d'))
    # aging_date_from = fields.Date(string="As of", default=lambda *a:(datetime.now() + timedelta(days=(6))).strftime('%Y-%m-%d'))

    period_length = fields.Integer(string="Period Length (days)", default=30)

    filter_per = fields.Selection(string="Filter", selection=[('gen', 'General'),('area','Area'),('prod','Product')], default='gen')

    prod_sel = fields.Many2one('product.template', string="Product")

    collector_sel = fields.Many2one('res.partner', string="Collector")

    area_list = fields.Many2many('config.barangay', string="Barangay")

    @api.onchange('collector_sel')
    def onchange_method(self):
        self.area_list = self.collector_sel.collector_area_id

    @api.multi
    def print_general_aging_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['aging_date_from', 'period_length','filter_per','prod_sel','area_list'])[0]
        # print data
        # aging_date_from =generate_general_aging data['form']['aging_date_from']
        # period_length = data['form']['period_length']
        # print aging_date_from, period_length
        generate_general_aging = self.env['general.aging'].search([])
        dt = data['form']['aging_date_from']
        pl = data['form']['period_length']
        for c in range(0, len(generate_general_aging)):
            generate_general_aging[c].get_days_passed(dt,pl)

        return self._print_report(data)

        # @api.multi
    # def print_general_aging_report(self):
    #     # self.ensure_one()
    #     data = {}
    #     data['ids'] = self.env.context.get('active_ids', [])
    #     data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
    #     data['form'] = self.read(['aging_date_from','period_length'])[0]
    #     print data
    #     return self._print_report(data)
    #

    def _print_report(self, data):
        # print 'test handler'
        # data['form'].update(self.read(['aging_date_from', 'period_length'])[0])
        # data = {}
        # data['form'] = self.read(['course_id', 'batch_id'])[0]
        return self.env['report'].get_action(self, 'brdc_inventory.general_aging_view', data=data)

    @api.multi
    def print_general_aging_cd_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['aging_date_from', 'period_length','filter_per','prod_sel','area_list'])[0]

        generate_general_aging_cd = self.env['general.aging_cd'].search([])
        dt = data['form']['aging_date_from']
        pl = data['form']['period_length']
        for c in range(0, len(generate_general_aging_cd)):
            generate_general_aging_cd[c].get_days_passed(dt,pl)

        return self._print_report_cd(data)

    def _print_report_cd(self, data):
        return self.env['report'].get_action(self, 'brdc_inventory.general_aging_cd_view', data=data)
