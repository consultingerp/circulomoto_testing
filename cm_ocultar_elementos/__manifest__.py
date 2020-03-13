# -*- coding: utf-8 -*-
{
    'name': "cm_ocultar_elementos",

    'summary': """
        Oculta elementos
        """,

    'description': """
        Oculta elementos:
        -Botón Actualizar cantidad a mano

    """,

    'author': "soluciones 4G",
    'website': "soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
    'base'
    ,'stock'
    ,],

    # always loaded
    'data': [
        'security/security.xml',
        'views/ocultar_qtybutton_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}

######NOTAS
#http://ingeniosolutions.com.ar/demos/pythagoreanodoo/acusmata/seguridad-basica-permisos-csv-grupo-de-usuarios
#https://odootips.com/saber-si-un-usuario-pertenece-a-un-grupo-1c30d34fdcf1
#https://stackoverrun.com/es/q/12285834