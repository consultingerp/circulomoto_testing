# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models


class pos_order_lines(models.Model):
	_inherit = 'pos.order.line'

	price_subtotal = fields.Float(store=True)
	x_proveedor_cmoto = fields.Char("Proveedor", compute='get_proveedor')
	
	x_proveedor = fields.Many2one(related="product_id.seller_ids.name",string='Proveedor',store=True)
	x_fecha_pedido = fields.Datetime(string='Fecha pedido',compute="get_date_order",store=True)

	@api.one
	@api.depends('order_id')
	def get_date_order(self):
		for record in self:
			record.x_fecha_pedido = record.order_id.date_order

	@api.multi
	def get_proveedor(self):
		for record in self:
			try:
				producto_id = record.product_id
				primer_proveedor = producto_id.seller_ids
				id_proveedor1 = primer_proveedor[0].name
				nproveedor = id_proveedor1.name
				nombreproveedor = nproveedor
				record.x_proveedor_cmoto = nombreproveedor
			except IndexError as e:
				record.x_proveedor_cmoto = "Sin Proveedor"
