# -*- coding: utf-8 -*-
{
    'name': "Info Asset",

    'summary': """
        Account Asset with asset types""",

    'description': """
        Account Asset functionality with different asset types and 
        customizations
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','om_account_asset'],

    # always loaded
    'data': [
        'data/infoasset_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/asset_group_views.xml',
        'views/asset_cia_category_views.xml',
        'views/asset_cia_impact_views.xml',
        'views/asset_classification_views.xml',
        'views/asset_views.xml',
        'views/infoasset_menu_views.xml',
    ],
}
