# -*- coding: utf-8 -*-
{
    'name': "Productos vendidos punto de venta",
    'description': "Se agrego el tipo de vista en lista para mostrar los productos vendidos en POS",
    'author': "Soluciones4g",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product','point_of_sale'],

    # always loaded
    'data': [
        'views/productos_vendidos_pos_view.xml'
    ],
    'installable':True,
    'auto_install':False,
}
