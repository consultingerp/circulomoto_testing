# -*- coding: utf-8 -*-
{
    'name': "CMoto Campo de marca",

    'summary': """
        Agregar campo de marca al modelo product.template""",

    'description': """
        Se agrega el campo de marca y se modifica el 
        campo de list_price en el formulario del producto.
    """,

    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded Recurde cargar deacuerdo al orden deseado
    'data': [
        #'views/mod_precio_field_view.xml',
        'views/cmoto_campomarca_view.xml',
        'views/item_marca_view.xml',
    ],
    'installable':True,
    'auto_install':False,
}
