# -*- coding: utf-8 -*-

from odoo import fields, models, api

class poCuentaAnalitica(models.Model):
    _inherit = 'purchase.order'
    x_cuenta_analitica_id = fields.Many2one('account.analytic.account',string='Cuenta Analitica')
    x_cuentas = fields.Char(string='Cuentas')
