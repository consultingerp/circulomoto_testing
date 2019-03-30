# -*- coding: utf-8 -*-
{
    'name': "ihm_ocultar_validar",

    'summary': """
        Solo muestra el boton validar a un usuario específico""",

    'description': """
        Sólo muestra el boton validar a un usuario específico
        el grupo se genera en el archivo security,
        los usuarios se deberán agregar manualmente al grupo validacion_factura
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
    ,'account'
    ,'account_accountant'
    ,],

    # always loaded
    'data': [
        'security/security.xml',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}

######NOTAS
#http://ingeniosolutions.com.ar/demos/pythagoreanodoo/acusmata/seguridad-basica-permisos-csv-grupo-de-usuarios
#https://odootips.com/saber-si-un-usuario-pertenece-a-un-grupo-1c30d34fdcf1
#https://stackoverrun.com/es/q/12285834