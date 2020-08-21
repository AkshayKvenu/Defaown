# -*- coding: utf-8 -*-
{
    'name': "Info CMDB",

    'summary': """
        Info CMDB """,

    'description': """
        Info CMDB
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': ['base','om_account_asset','stock','hr','resource'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/cmdb_relationship_class_views.xml',
        'views/cmdb_relationship_type_views.xml',
        'views/cmdb_class_category_views.xml',
        'views/cmdb_groups_views.xml',
        'views/infocmdb_business_service_views.xml',
        'views/infocmdb_devices_views.xml',
        'views/infocmdb_software_licenses_views.xml',
        'views/menu_info_cmdb.xml',
        'views/infocmdb_favicons_devices_views.xml',
    ],
}
