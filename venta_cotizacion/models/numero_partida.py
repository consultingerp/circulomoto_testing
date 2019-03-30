# -*- coding: utf-8 -*-

from odoo import fields, models, api

class numeroPartida(models.Model):
	_inherit = 'sale.order.line'
	x_num_partida = fields.Integer(string='# Partida')

	@api.onchange('product_uom_qty', 'product_uom', 'route_id')
	def _onchange_product_id_check_availability(self):
		if not self.product_id or not self.product_uom_qty or not self.product_uom:
			self.product_packaging = False
			return {}
		if self.product_id.type == 'product':
			return {}
		return {}

class amountToTextSale(models.Model):
	_inherit = 'sale.order'
	x_vigencia = fields.Char(string='Vigencia Cotizacion')
	@api.multi
	def _amount_to_text(self):
		"""Method to transform a float amount to text words
		E.g. 100 - ONE HUNDRED
		:returns: Amount transformed to words mexican format for invoices
		:rtype: str
		"""
		self.ensure_one()
		currency = self.currency_id.name.upper()
		# M.N. = Moneda Nacional (National Currency)
		# M.E. = Moneda Extranjera (Foreign Currency)
		currency_type = 'M.N' if currency == 'MXN' else 'M.E.'
		# Split integer and decimal part
		amount_i, amount_d = divmod(self.amount_total, 1)
		amount_d = round(amount_d, 2)
		amount_d = int(amount_d * 100)
		words = self.currency_id.with_context(lang=self.partner_id.lang or 'es_ES').amount_to_text(amount_i).upper()
		invoice_words = '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(
			words=words, amount_d=amount_d, curr_t=currency_type)
		return invoice_words