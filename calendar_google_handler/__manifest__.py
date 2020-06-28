# -*- coding: utf-8 -*-
{
    'name': "calendar_google_handler",

    'summary': """
        Read events from list of google calender.
        Create calendar and event entries according to config settings.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "robert@redcor.ch",
    'website': "http://www.redo2oo.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'calendar',
        'event',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
