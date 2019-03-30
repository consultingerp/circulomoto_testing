# -*- coding: utf-8 -*-

from odoo import fields, models, api


class stockQuantTransfer(models.TransientModel):
	_name = 'stock.quant.transfer'

	location_id = fields.Many2one('stock.location',string='Ubicación Origen',
		default=lambda self: self.env.context.get('location_id'),readonly=True)
	location_dest_id = fields.Many2one('stock.location',string='Ubicación Destino',required=True)
	product_id = fields.Many2one('product.product',string='Producto',default=lambda self: self.env.context.get('product_id'),readonly=True)
	qty = fields.Float(string='Cantidad',default=lambda self: self.env.context.get('quantity'))
	lot_id = fields.Many2one('stock.production.lot', 'Lote/Nº de serie', default=lambda self: self.env.context.get('lot_id'),domain="[('product_id','=',product_id)]")

	def transfer_product_qty(self):
		order_lines = []
		for record in self:
			picking_type = self.env['stock.picking.type'].search([('name', '=', record.location_id.name)])
			project = self.env['project.project'].search([('name', '=', record.location_id.name)])
			order_lines.append((0,0,{
					'state':'done',
					'name':record.product_id.name,
					'date_expected':fields.Datetime.now(),
					'product_id':record.product_id.id,
					'product_uom_qty':record.qty,
					'quantity_done':record.qty,
					'product_uom':record.product_id.uom_id.id,
					'x_proyecto':project.id
				}))
			print('order lines',order_lines)
			vals = {
				'state':'done',
				'location_id':record.location_id.id,
				'location_dest_id':record.location_dest_id.id,
				'picking_type_id': picking_type.id,
				'move_lines': order_lines, 
				'move_type': 'direct',
				'priority': '1',
				'x_cuenta_analitica':project.id,
			}
			print('CALS',vals)
			res = self.env['stock.picking'].create(vals)
		return res