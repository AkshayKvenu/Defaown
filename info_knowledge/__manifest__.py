# -*- coding: utf-8 -*-
{
    'name': "Info Knowledge",

    'summary': """
        Info Knowledge""",

    'description': """
        Info Knowledge
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','info_cmdb'],

    # always loaded
    'data': [
        'data/ir_sequence_data.xml',
        'security/security_knowledge.xml',
        'security/ir.model.access.csv',
        'views/info_knowledge_views.xml',
        'views/menu_info_knowledge.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
