# -*- coding: utf-8 -*-
from odoo import fields, models

class Cmoto_modelomarcas(models.Model):
	_name = 'x_cmoto.marcas'

	name = fields.Char(string="Nombre de la marca")