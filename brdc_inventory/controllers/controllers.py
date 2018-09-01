# -*- coding: utf-8 -*-
from odoo import http

# class SerialBrdc(http.Controller):
#     @http.route('/brdc_inventory/brdc_inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/brdc_inventory/brdc_inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('serial_brdc.listing', {
#             'root': '/brdc_inventory/brdc_inventory',
#             'objects': http.request.env['brdc_inventory.brdc_inventory'].search([]),
#         })

#     @http.route('/brdc_inventory/brdc_inventory/objects/<model("brdc_inventory.brdc_inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('serial_brdc.object', {
#             'object': obj
#         })