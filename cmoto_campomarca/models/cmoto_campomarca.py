# -*- coding: utf-8 -*-
from odoo import fields, models

class Cmoto_campomarca(models.Model):
	_inherit = 'product.template'

	x_cmoto_marca = fields.Many2one('x_cmoto.marcas', string="Marca")