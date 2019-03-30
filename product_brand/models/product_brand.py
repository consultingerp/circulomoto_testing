# -*- coding: utf-8 -*-

from odoo import fields, models

class productBrand(models.Model):
    _name = 'product.brand'

    name = fields.Char(string='Marca',required=False)

class productTemplate(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand',string='Marca')