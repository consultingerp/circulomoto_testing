# -*- coding: utf-8 -*-
import base64
import io
import logging
from PIL import Image, ImageFont, ImageDraw
from odoo import http, tools
from odoo.http import request

logger = logging.getLogger(__name__)


class ImportProductImages(http.Controller):

    @http.route('/page/import_product_images.import_product_images', type='http', auth='user', website=True)
    def render_website_template(self):
        is_manager = False
        user = request.env.user
        inventory_manager_group = http.request.env.ref('stock.group_stock_manager')
        if user.id in inventory_manager_group.users.ids:
            is_manager = True
            print ("Usuario admin de inventario")
        return http.request.render('import_product_images.import_product_images',
                                   {'is_manager': is_manager}
                                   )

    @http.route('/page/import_product_images.images_success', type='http', auth='user', website=True)
    def render_images_success(self):
        return http.request.render('import_product_images.images_success', {})

    @http.route('/page/import_product_images.images_failed', type='http', auth='user', website=True)
    def render_images_failed(self):
        return http.request.render('import_product_images.images_failed', {})

    @http.route('/website/import_images', type='http', auth='user', website=True, methods=['POST'])
    def import_product_images(self, product_images=None, disable_optimization=None, **kwargs):
        if not product_images:
            print ("There're no images to load")
        else:
            try:
                total_images = 0
                images_per_product = 0
                for c_file in request.httprequest.files.getlist('product_images'):
                    total_images += 1
                    image_data = c_file.read()

                    # Search product by internal reference
                    default_code = c_file.filename.split(".")
                    file_name_product = default_code[0].strip()

                    product_obj = http.request.env['product.template'].sudo().search(
                        [
                            ('images_code', '=', file_name_product)
                        ]
                    )

                    if product_obj:
                        images_per_product += 1
                        processed_image = base64.b64encode(image_data)
                        product_obj.sudo().write(
                            {
                                'image_medium': processed_image
                            }
                        )
                if images_per_product > 0:
                    print ("\n Total images to load")
                    print (total_images)
                    print ("\n Images Loaded")
                    print (images_per_product)
                    return http.request.redirect('/page/import_product_images.images_success')
                else:
                    return http.request.redirect('/page/import_product_images.images_failed')
            except Exception as e:
                logger.exception("Failed to upload images")
