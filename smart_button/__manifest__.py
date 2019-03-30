# -*- coding: utf-8 -*-
{
    'name': "Agregar smart button",

    'summary': """
    Agregar smart button a los clientes para levantar ticket
    """,

    'description': """
        Agregar campo relacionado con helpdesk
    """,

    'author': "Soluciones4g",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','crm','helpdesk'],

    # always loaded
    'data': [
        'views/add_button_partner.xml',
    ],
    'installable':True,
    'auto_install':False,
}
