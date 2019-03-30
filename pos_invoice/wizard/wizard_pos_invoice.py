# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo import api
from odoo import fields
from odoo import models
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
import time
from openerp.exceptions import except_orm

class ClassName(models.TransientModel):
    _name = 'wizard.pos.invoice'
    
    #regresa el número de elementos seleccionados
    @api.model
    def _count(self):
        #print("Hello_count")
        return len(self._context.get('active_ids', []))
    
    @api.model
    def _get_advance_payment_method(self):
        print("Hello_get_advance_payment")
        if self._count() == 1: ##POR QUE SOLO IGUAL A UNO, SI HAY MAS SELECCIONADOS NO LO HACE
            #print("HELLO IF COUNT")
            sale_obj = self.env['pos.order']
            order = sale_obj.browse(self._context.get('active_ids'))[0] ##POR QUE SOLO LA POSISION [0]?????
            if all([line.product_id.invoice_policy == 'order' for line in order.lines]): #LINE ES UNA VARIABLE PARA ITERAR order.lines
                #print("HELLO IF ALL")
                return 'all'
        #print("NO IF :::")
        return 'delivered'

    advance_payment_method = fields.Selection([
                                              ('delivered', 'Lineas de factura'),
                                              ('all', 'Lineas de factura 1'),
                                              #('percentage', 'Deposito (porcentaje)'),
                                              #('fixed', 'Deposito (cantidad fija)')
                                              ], string='¿Que quiere facturar?', default=_get_advance_payment_method, required=True)
    count = fields.Integer(default=_count, string='# de Ordenes')

    @api.onchange('advance_payment_method')
    def onchange_advance_payment_method(self):
        #print("Hello_onchamge_advance_payment")
        if self.advance_payment_method == 'percentage':
            return {'value': {'amount': 0}}
        return {}

    @api.multi
    def create_invoices(self):
        validacion = True
        print("Hello_create_invoices:::::::::::::::::::::::::::::::::::::::::::")
        sale_orders = self.env['pos.order'].browse(self._context.get('active_ids'))#LE QUITÉ CORCHETES!!!!!

        for record in sale_orders:
            #print("iterando[][][][][][][][[][", record.id)
            if str(record.state) == 'invoiced':#invoiced - done  or str(record.state) == 'done'
                print('Seleccion incorrecta: Solo se deben seleccionar Pagados')
                validacion = False

        if validacion:
            if self.advance_payment_method == 'delivered': #
                sale_orders.action_invoices_create()
            elif self.advance_payment_method == 'all':
                sale_orders.action_invoices_create()
            return {'type': 'ir.actions.act_window_close'}
        else:
            #print('NO SE PROCESA::::::::')
            raise except_orm(_('Error'),
                 _('Se debe cancelar esta operación, selecciona únicamente pedidos en estado <Pagado>'))
                 #https://poncesoft.blogspot.com/2016/05/pop-up-ventanas-emergentes-odoo.html
