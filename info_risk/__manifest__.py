# -*- coding: utf-8 -*-
{
    'name': "Info Risk",

    'summary': """
        Info Risk""",

    'description': """
        Info Risk
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.5',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','info_control','web_widget_colorpicker'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/info_risk_wizard_views.xml',
        'views/view.xml',
        'views/info_risk_config_view.xml',
        'views/risk_scenario_menu_views.xml',
        'views/risk_management_views.xml',
        'views/res_config_settings.xml',
        'views/menu_info_risk.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/response_demo.xml',
    ],
}
