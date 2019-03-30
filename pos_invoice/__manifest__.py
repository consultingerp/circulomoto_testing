# -*- coding: utf-8 -*-
{
    'name': 'Wizard Facturas',
    'version': '10.0.1.0.0',
    'description': """Crear Facturas a partir de diferentes Pedidos de Punto de Venta""",
    'author': 'FMQ',
    'depends': ['base', 'account', 'point_of_sale'],
    'data': ['wizard/wizard_pos_invoice_view.xml'],
    'installable': True,
    'application': False,
}
