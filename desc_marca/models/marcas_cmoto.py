# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Marcas_cmoto(models.Model):
    _name = 'cmoto_marcas.marcas'

    name = fields.Char(string="Nombre de la marca", required=True)
