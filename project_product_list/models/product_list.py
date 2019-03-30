# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import fields, models, api

class productList(models.Model):
	_name = 'product.list'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	project_id = fields.Many2one('project.project',string='Proyecto',
		default=lambda self: self.env.context.get('default_project_id'),
		track_visibility='onchange',readonly=True)
	field_bool = fields.Boolean(default=False)
	product_list_ids = fields.One2many('product.list.line','product_list_id',string='Productos')
	pruchase_order_id = fields.Many2one('purchase.order')
	state = fields.Selection([
		('draft', 'En Elaboración'),
		('confirmed', 'En Validación'),
		('done', 'Lista Validada'),
		('purchase','RFQ Generada')
	], default='draft', readonly=True, track_visibility='onchange')
	name = fields.Char(string='Nombre',required=True)
	date = fields.Datetime(string='Fecha Requerida',default=fields.Datetime.now,required=True)
	type = fields.Selection(selection=[('alta','Alta'),('normal','Normal'),('baja','Baja')],
		track_visibility='onchange')
	is_locked = fields.Boolean(default=True)

	@api.multi
	def set_done(self):
		for record in self:
			locations = self.env.ref('stock.stock_location_stock').id
			parent = self.env['stock.location'].browse(locations)
			location_customers = self.env.ref('stock.stock_location_customers').id
			parent_out = self.env['stock.location'].browse(location_customers)
			location = self.env['stock.location'].search([('name', '=', record.project_id.name)])
			location_out = self.env['stock.location'].search([('name', '=', record.project_id.name+'out')])
			print('LOCATION',location)
			if not location and not location_out:
				location = self.env['stock.location'].create({
						'name': record.project_id.name,
						'usage':'internal',
						'location_id':parent[0].id
					})
				location_out = self.env['stock.location'].create({
						'name': record.project_id.name+'out',
						'usage':'customer',
						'location_id':parent_out[0].id
					})
			#location_in = self.env['stock.location'].search(['&',('name', '=', record.project_id.name),('usage', '=','internal' )])
			print('LOCATION AFTER CREATE',location)
			record.location_id = location
			record.location_id.location_id = parent
		for l in self.location_id:
			picking = self.env['stock.picking.type'].search(['|',('name', '=', self.project_id.name),('name', '=', self.project_id.name+'out')])
			l_out = self.env['stock.location'].search([('name', '=', self.project_id.name+'out')])
			if not picking:
				picking_type = self.env['stock.picking.type'].create({
					'name':self.project_id.name,
					'sequence_id':18,
					'code':'internal',
					'default_location_src_id':l.location_id.id,
					'default_location_dest_id':l.id
				})
				picking_type_out = self.env['stock.picking.type'].create({
					'name':self.project_id.name+'entrega',
					'sequence_id':16,
					'code':'outgoing',
					'default_location_src_id':l.id,
					'default_location_dest_id':l_out.id
				})
		self.state = 'done'
		self.write({'is_locked':True})

	location_id = fields.Many2one("stock.location", string="Almacén Origen")

	@api.multi
	def set_confirm(self):
		for record in self.product_list_ids:
			record.product.sudo().write({'x_qty_list':record.cantidad})
			record.product.sudo().write({'x_task':record.task_id.id})
			record.product.sudo().write({'x_fecha_requerida':record.fecha})
			record.product.sudo().write({'x_seleccion':record.type})
			print('FECHA ',record.product.x_fecha_requerida)
			print('SELECTION TYPE',record.type)
		#self.generar_orden_compra()
		self.state = 'confirmed'
		self.write({'is_locked':True})

	@api.multi
	def set_draft(self):
		self.state = 'draft'

	@api.multi
	def generar_orden_compra(self):
		seller_by_product_mxn = defaultdict(set)
		seller_by_product_usd = defaultdict(set)
		seller_products_mxn = defaultdict(set)
		seller_products_usd = defaultdict(set)
		usd = []
		mxn = []
		usd_seller = []
		mxn_seller = []
		for record in self.product_list_ids:
			
			if record.supplier_id.id != False:
				if record.supplier_id.currency_id.name == 'MXN':
					seller_by_product_mxn[record.supplier_id.name.id].add(record.product.id)
					mxn.append(record.supplier_id.currency_id.id)
					print('PROVEEDOR PREFERIDO CON MXN',seller_by_product_mxn)
				elif record.supplier_id.currency_id.name == 'USD':
					seller_by_product_usd[record.supplier_id.name.id].add(record.product.id)
					usd.append(record.supplier_id.currency_id.id)
					print('PROVEEDOR PREFERIDO CON USD',seller_by_product_usd)
				
			else:
				for vendor in record.product.seller_ids:
					if vendor.currency_id.name == 'MXN':
						seller_products_mxn[vendor.name.id].add(record.product.id)
						mxn_seller.append(vendor.currency_id.id)
						print('PROVEEDORES MXN',seller_products_mxn)
					elif vendor.currency_id.name == 'USD':
						seller_products_usd[vendor.name.id].add(record.product.id)
						usd_seller.append(vendor.currency_id.id)
						print('PROVEEDORES USD',seller_products_usd)

		for seller_mxn in seller_by_product_mxn.items():
			print('FOR PROVEEDOR PREFERIDO MXN',seller_mxn)
			self.purchase_order(seller_mxn[0],seller_mxn[1],mxn[0])

		for seller_usd in seller_by_product_usd.items():
			print('FOR PROVEEDOR PREFERIDO MXN',seller_usd)
			self.purchase_order(seller_usd[0],seller_usd[1],usd[0])

		for vendor_mxn in seller_products_mxn.items():
			print('FOR PROVEEDORES MXN',vendor_mxn)
			print('FOR PROVEEDORES MXN',mxn_seller)
			self.purchase_order(vendor_mxn[0],vendor_mxn[1],mxn_seller[0])

		for vendor_usd in seller_products_usd.items():
			print('FOR PROVEEDORES USD',vendor_usd)
			print('FOR PROVEEDORES USD',usd_seller)
			self.purchase_order(vendor_usd[0],vendor_usd[1],usd_seller[0])

	def purchase_order(self,seller,producto,currency_id):
		supplier = self.env['res.partner'].browse(seller)
		proyecto_id = self.project_id
		picking = self.env['stock.picking.type'].search([('name', '=', proyecto_id.name)])
		vals = {
			'date_order':fields.Datetime.now(),
			'x_cuenta_analitica_id':proyecto_id.id,
			'partner_id':supplier.id,
			'picking_type_id':picking.id,
			'currency_id':currency_id
		}
		print('purchase -<<<<<<',str(vals))
		res = self.env['purchase.order'].create(vals)

		for products in producto:
			product = self.env['product.product'].browse(products)
			
			vals_order_line = {
				'order_id':res.id,
				'x_prioridad':product.x_seleccion,
				'product_id':product.id,
				'name':product.name,
				'x_proyecto':proyecto_id.id,
				'x_tarea':product.x_task,
				'product_qty':product.x_qty_list,
				'date_planned':product.x_fecha_requerida,
				'product_uom':product.uom_id.id,
				'price_unit':1.0
			}
			print(str(vals_order_line))
			res_line = self.env['purchase.order.line'].create(vals_order_line)
		r = self.pruchase_order_id
		r = res
		self.field_bool = True
		self.write({'is_locked':True})
		self.state = 'purchase'
		return r, res_line


class productListLine(models.Model):
	_name = 'product.list.line'

	product_list_id = fields.Many2one('product.list')
	product = fields.Many2one('product.product',string='Productos',required=True)
	supplier_id = fields.Many2one('product.supplierinfo',string='Proveedores',domain="[('product_tmpl_id.id', '=', product)]")
	project_id = fields.Many2one('project.project',
		default=lambda self: self.env.context.get('default_project_id'),store=True)
	task_id = fields.Many2one('project.task',store=True)
	marca = fields.Char(string='Marca',compute="get_marca")
	modelo = fields.Char(string='Modelo',compute="get_modelo")
	precio = fields.Float(string='Costo',compute="get_precio")
	cantidad = fields.Float(string='Cantidad')
	uom_lista = fields.Many2one('product.uom', string="Unidad de medida", 
		related='product.uom_id',required=True,readonly=True)
	name = fields.Text(string='Notas')
	fecha = fields.Datetime(string='Fecha Requerida',default=fields.Datetime.now)
	type = fields.Selection(selection=[('alta','Alta'),('normal','Normal'),('baja','Baja')],string='Prioridad')
	state = fields.Selection([
		('draft', 'En Elaboración'),
		('confirmed', 'En Validación'),
		('done', 'Lista Validada'),
	], default='draft', readonly=True, related='product_list_id.state')

	@api.onchange('product')
	def get_marca(self):
		for record in self:
			record.marca = record.product.product_tmpl_id.brand_id.name
	
	@api.onchange('product')
	def get_modelo(self):
		for record in self:
			record.modelo = record.product.product_tmpl_id.modelo

	@api.onchange('product')
	def get_precio(self):
		for record in self:
			record.precio = record.product.product_tmpl_id.standard_price

class productProject(models.Model):
	_inherit = 'project.project'

	product_list_count = fields.Integer(compute="get_product_list_count")

	def get_product_list_count(self):
		list_data = self.env['product.list'].read_group([('project_id','in',self.ids)],['project_id'],['project_id'])
		mapped_data = dict((data['project_id'][0], data['project_id_count']) for data in list_data)
		for project in self:
			project.product_list_count = mapped_data.get(project.id, 0)

class productTask(models.Model):
	_inherit = 'product.product'

	x_task = fields.Integer(string='Field Label')
	x_qty_list = fields.Integer(string='Field Label')
	x_seleccion = fields.Char(string='Filed Label')
	x_fecha_requerida = fields.Datetime(string='Field Label')