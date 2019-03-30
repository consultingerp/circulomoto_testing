# -*- coding: utf-8 -*-
{
    'name': "Lista de Productos",
    'description': """
        Generar diferentes listas de productos
    """,
    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",
    'version': '0.1',
    'depends': ['base','product','project','purchase','stock'],
    'data': [
        'wizard/stock_quant_transfer_view.xml',
        'views/product_list_view.xml',
        'views/stock_picking_project.xml',
        'wizard/delete_rfq_view.xml',
        'views/estatus_rfq_view.xml',
        ],
    'installable':True,
    'auto_install':False,
}
