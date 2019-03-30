# -*- coding: utf-8 -*-
{
    'name': 'Ticket Devolucion POS',
    'version': '10.0.1.0',
    'description': """Ticket Devolucion""",
    'author': 'S4G',
    'company': 'Soluciones 4G',
    'website': 'http://www.oluciones4g.com',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/report_receipt_view.xml',
        'views/report_ticket.xml',
        'views/pos_invisible_refund_view.xml',
        'views/inherit_internal_layout.xml'
    ],
    'installable': True,
    'auto_install': False,

}
