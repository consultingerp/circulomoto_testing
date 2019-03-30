# -*- coding: utf-8 -*-
{
    'name': "Import product image",

    'summary':
        """
            * Import product images from website.
            * Default code set as required
        """,

    'description':
        """
            * A user can load the product images from the website,
                the user must be inventory manager.
            * With this module you can import images for the products,
                the name of the image must be the same as the default code of the product
        """,

    'author': "Soluciones4G - OGM",
    'website': "www.soluciones4g.com",
    'license': 'AGPL-3',

    'category': 'Extra Tools',
    'version': '0.1',

    'depends': [
        'base',
        'web',
        'website_form',
        'stock',
        'product',
    ],

    'demo': [],

    'data': [
        'views/product_views_inherited.xml',
        'static/src/xml/website_resources.xml',
        'views/import_product_images_templates.xml',
        'views/data.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
