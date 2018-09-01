# -*- coding: utf-8 -*-
{
    'name': "brdc_inventory",

    'summary': """A Small Description""",

    'description': """
        No purpose at all
    """,

    'author': "MGC",
    'website': "http://www.mutigroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','purchase','loan_application','loan_information', 'brdc_account','brdc_security'],
    # 'depends': ['base','stock','purchase'],
    # ,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/config_area.xml',
        'views/grave_type_list.xml',
        'views/cremation_order.xml',
        'views/interment_order.xml',
        'views/inherited_account_invoice.xml',
        'views/inherited_product_product_view.xml', # enable ni
        'views/inherited_product_template_view.xml',
        'views/inherited_sale_order_line.xml',
        'views/inherited_stock_inventory_line.xml',
        'views/inherited_stock_production_lot_tree.xml',
        'views/inherited_stock_production_lot.xml',
        'views/init_config.xml',
        'views/deceased_list.xml',
        'views/other_info_config.xml',
        'views/inherited_stock_pack_operation.xml',
        'views/general_aging_of_receivables.xml',

        # 'views/employee_hierarchy.xml',
        # 'views/employee_commission.xml',
        # 'views/agent_commission_line.xml',

        'reports/customer_ledger_report.xml',
        'reports/statement_of_account_report.xml',
        'views/report_general_aging.xml',
        'reports/general_aging_view.xml',
        'reports/general_aging_cd_view.xml',
        'reports/agent_list_report.xml',
        # 'reports/print_buttons.xml'
        'views/lot_generator_handler.xml',
        'views/collector_area.xml',
        # 'views/inherited_res_partner.xml', usab temporarily
        'views/sold_product_per.xml',
        'reports/sold_lots_per_report.xml',
        'views/menu_items.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}