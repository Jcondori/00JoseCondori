# -*- coding: utf-8 -*-
{
    'name': "Jcondori Module",

    'summary': """
        Modulo para practicar odoo""",

    'description': """
        Modulo para practicar odoo
    """,

    'author': "Jose Luis Condori Jara",
    'website': "https://jcondori.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Personalization',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menuitem.xml',
        'views/hospital_patient_view.xml',
        'views/hospital_category_view.xml',
        'views/hospital_consult_view.xml',
        'views/hospital_consult_invoice_view.xml',
        'views/account_move_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
