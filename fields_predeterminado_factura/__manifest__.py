# -*- coding: utf-8 -*-
{
    'name': "factura editable y default campos agregados",

    'summary': """editable y default
    """,

    'description': """
        Modulo para facturacion para que campo sea editable pero lance por dafault un valor
    """,

    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'contacts',
        'account'
        ],

#       'purchase',       
    #       'contacts',
    #       'stock',
  

        # always loaded
            'data': [#'views/fabricacion_editableDview.xml',
                'security/ir.model.access.csv',
                'data/transferencia_usos.xml',
                'views/contactos_datos.xml',
              
    
        ],
            'demo':[

            ],
        'installable':True,
}
