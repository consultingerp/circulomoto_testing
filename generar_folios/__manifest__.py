# -*- coding: utf-8 -*-
{
    'name': "Generar Folios",

    'summary': """
        Generación de Folios personalizados
        """,

    'description': """
        Generación de Folios personalizados
    """,

    'author': "Soluciones4G MC",
    'website': '',

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'security/generar_folios_groups.xml',
        'demo/formatos_folios_demo.xml',
        'views/generar_folios_view_tree.xml',
        'views/generar_tipo_folio.xml',
        'views/menu.xml',
    ],

    'installable': True,
    'auto_install': False,
}
