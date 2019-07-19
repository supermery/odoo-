# -*- coding: utf-8 -*-
{
    'name': "Salon Module For Atlas Servair",

    'summary': """Salon Module For Atlas Servair""",
    'author': "R&B Consulting",
    'website': "https://www.r-bconsulting.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'website', 'website_sale', 'sale', 'operating_unit','mrp_atlas_servair'],

    'data': [
        
        'views/as_salon.xml',
        # 'views/as_contract.xml',
        #'views/website_salon.xml',
        'views/website_products.xml',
        'views/sale_order_view.xml',
        # 'views/mrp_bom_views.xml',
        'security/ir.model.access.csv',
        'views/add_to_chart.xml',
    ],
}