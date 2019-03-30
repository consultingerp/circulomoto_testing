# -*- coding: utf-8 -*-

from odoo import fields, models, api

class fieldRepair(models.Model):
	_inherit = 'mrp.repair'
	
	@api.onchange('location_id')
	def onchange_location_id(self):
		customer = self.env['stock.location'].search(['|',('name','=','Clientes'),('usage','=','customer')],limit=1)
		self.location_dest_id = customer[0].id

class MrpRepairLineLocation(models.Model):
	_inherit = 'mrp.repair.line'
	
	@api.multi
	def _get_location_customer_repair(self):
		customer = self.env.ref('stock.stock_location_customers').id
		return customer

	location_dest_id = fields.Many2one('stock.location', 'Dest. Location',index=True, required=True,default=_get_location_customer_repair)
