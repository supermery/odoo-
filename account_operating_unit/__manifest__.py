# -*- coding: utf-8 -*-
{
    'name': 'Account Operating Unit',
    'version': '1.1',
    'category': 'Accounting & Finance',
    'summary': 'Account Operating Unit',
    'description': "",
    'website': 'https://www.r-bconsulting.com',
    'images': [
    ],
    'depends': [
        'account',
        'operating_unit',
        'analytic_operating_unit'
    ],
    'data': [
        #report
        'report/account_generalledger_report.xml',
        'report/report_financial.xml',
        'report/report_trial_balance.xml',
        #views
        'views/account/account_invoice_views.xml',
        'views/account/account_journal_views.xml',
        'views/account/account_move_views.xml',
        'views/account/account_payment_views.xml',
        'views/base/res_company_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'qweb': [],
}