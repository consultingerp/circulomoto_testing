# -*- coding: utf-8 -*-
{
    'name': "CMoto Reporte Marca",

    'summary': """
        Muestra el precio promedio en el reporte inventario""",

    'description': """
        Muestra el precio promedio en el reporte inventario
    """,

    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
    'stock',],

    # always loaded Recurde cargar deacuerdo al orden deseado
    'data': [
        'views/report_inherit_tree2.xml',
    ],
    'installable':True,
    'auto_install':False,
}
