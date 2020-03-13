# -*- coding: utf-8 -*-
from odoo import api
from odoo import fields
from odoo import models
# modelo de campos a editar desde factura borrados

class editable_invoice(models.Model):
	_inherit = 'account.invoice'


	@api.model
	def create(self, vals):
		factura=super(editable_invoice,self).create(vals)
		print("hola2")
		id_x= self.env['res.partner'].search([('id', '=', factura.partner_id.id)])
		print("hola probando metodo")
		print(id_x.type)
		print(factura.purchase_id.id)
		print(factura.origin)

		if factura.origin:

			if(id_x.parent_id.id):
				
				print(id_x.type)
				print(id_x.parent_id.id)
				id_matrix= self.env['res.partner'].search([('id', '=', id_x.parent_id.id)])
				print(id_x.Transferenciaelectronica_Uso)
				factura.write({'l10n_mx_edi_partner_bank_id': id_matrix.Banco_asociado.id,'l10n_mx_edi_payment_method_id':id_matrix.Metodo_pago.id,
			   	'l10n_mx_edi_usage':id_matrix.Transferenciaelectronica_Uso }) 
			else:
				print("id_x.type == False")
				print(id_x.type)
				print(id_x.Transferenciaelectronica_Uso)
				factura.write({'l10n_mx_edi_partner_bank_id': id_x.Banco_asociado.id,'l10n_mx_edi_payment_method_id':id_x.Metodo_pago.id,
			       	'l10n_mx_edi_usage':id_x.Transferenciaelectronica_Uso }) #se utiliza el valor del select para pasar el tipo que es y deben tener el mismo valor que el original

		return factura



	@api.onchange('partner_id')
	def onchange_cliente(self):
		id_x= self.env['res.partner'].search([('id', '=', self.partner_id.id)])
		if(id_x.parent_id.id):#se busca si tiene padre el contacto porque si es asi se busca los datos del padre
				
			print(id_x.type)
			print(id_x.parent_id.id)
			id_matrix= self.env['res.partner'].search([('id', '=', id_x.parent_id.id)])
			print(id_x.Transferenciaelectronica_Uso)
			self.l10n_mx_edi_partner_bank_id=id_matrix.Banco_asociado.id
			self.l10n_mx_edi_payment_method_id=id_matrix.Metodo_pago.id
			self.l10n_mx_edi_usage=id_matrix.Transferenciaelectronica_Uso
		#	factura.write({'l10n_mx_edi_partner_bank_id': id_matrix.Banco_asociado.id,'l10n_mx_edi_payment_method_id':id_matrix.Metodo_pago.id,
		#	'l10n_mx_edi_usage':id_matrix.Transferenciaelectronica_Uso }) 
		else:
			print("id_x.type == False")
			print(id_x.type)
			print(id_x.Transferenciaelectronica_Uso)
			self.l10n_mx_edi_partner_bank_id=id_x.Banco_asociado.id
			self.l10n_mx_edi_payment_method_id=id_x.Metodo_pago.id
			self.l10n_mx_edi_usage=id_x.Transferenciaelectronica_Uso
		#	factura.write({'l10n_mx_edi_partner_bank_id': id_x.Banco_asociado.id,'l10n_mx_edi_payment_method_id':id_x.Metodo_pago.id,
		#	'l10n_mx_edi_usage':id_x.Transferenciaelectronica_Uso }) #se utiliza el valor del select para pasar el tipo que es y deben tener el mismo valor que el original





	# @api.onchange('amount', 'precio_unit')
 #    def _onchange_price(self):
 #        self.precio=self.amount * self.precio_unit
 #        return{
 #            'warning':{
 #                'title':"something bad happened",
 #                'message':"it was very bad indeed",
 #            }
 #        }