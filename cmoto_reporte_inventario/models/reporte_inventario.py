# -*- coding: utf-8 -*-
from odoo import fields
from odoo import models

class CmotoReporteInventario(models.Model):
    _inherit = 'product.product'

    def _calcula_valor_promedio(self):
        for record in self:
            record.x_valor_promedio = record.stock_value / record.qty_at_date
    
    
    x_valor_promedio = fields.Float(string="Valor promedio", 
                                    compute='_calcula_valor_promedio')
                                    
class StockQuantClass(models.Model):
    _inherit = 'stock.quant'
    
    def _calcula_valor(self):
        for record in self:
            record.x_valor = record.x_valor_promedio_related * record.quantity
            
    x_valor_promedio_related = fields.Float(string="Valor promedio", 
                                            related='product_id.x_valor_promedio'
                                            )
    x_valor = fields.Float(string="Valor", 
                           compute='_calcula_valor')
