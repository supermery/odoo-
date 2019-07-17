# -*- coding: utf-8 -*-
{
    'name': "Operating Unit Module",

    'summary': """
        operating_unit_module""",

    'description': """
        operating_unit_module
    """,

    'author': "R&B Consulting",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'crm',
        'sale',
        'sale_management',
        'account_accountant',
        'account',
        'purchase',
        'stock',
        'hr',
        'hr_contract',
        'hr_payroll',
        'hr_expense',
        'hr_payroll_account',
        'operating_unit',
        'account_operating_unit',
    ],

    # always loaded
    'data': [
        #data
        #security

        #views
        'views/account_reports/search_template_view.xml',
        'views/account_reports/report_financial.xml',
        'views/account_reports/account_report_views.xml',
        'views/account/account_invoice_views.xml',
        'views/sale/sale_order_views.xml',
        'views/sale/sale_report_view.xml',
        'views/purchase/purchase_order_views.xml',
        'views/stock/stock_warehouse_views.xml',
        'views/stock/stock_location_views.xml',
        'views/stock/stock_picking_views.xml',
        'views/stock/stock_move_views.xml',
        'views/hr/hr_contract_views.xml',
        'views/hr/hr_expense_views.xml',
        'views/hr/hr_expense_sheet_views.xml',
        'views/hr/hr_payslip_views.xml',

        #wizards

        # reports
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}