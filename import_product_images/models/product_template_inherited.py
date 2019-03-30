# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    images_code = fields.Char(
        string="Images code",
        compute="setimagescode",
        default='XXXXX00001',
        store=True,
    )

    @api.multi
    def setimagescode(self):
        for record in self:
            product_name = record.name
            product_reference = product_name.split(",")
            record.images_code = str(product_reference[-1].strip()).encode('utf-8')
