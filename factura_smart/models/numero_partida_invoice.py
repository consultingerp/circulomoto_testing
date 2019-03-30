# -*- coding: utf-8 -*-

from odoo import fields, models, api

class numeroPartidaInvoiceLine(models.Model):
	_inherit = 'account.payment'

	rfc_ordenante = fields.Char(string='RFC Cuenta Ordenante')
	cta_ordenante = fields.Char(string='Cuenta Ordenante')
	rfc_beneficiaro = fields.Char(string='RFC Cuenta Beneficiaria')
	cta_beneficiaro = fields.Char(string='Cuenta Beneficiaria')