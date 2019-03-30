# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Wizard_descuento(models.TransientModel):
    _name = 'desc_marca.wizard'

    Descuento = fields.Float(string="Descuento")
    Productos = fields.Many2many('product.product', string="Productos")
    Tarifa = fields.Many2one('product.pricelist', string="Aplicar a", required=True)

    @api.multi
    def agregar(self):
        for i in self.Productos:
            self.env.cr.execute(" INSERT INTO product_pricelist_item (applied_on, product_tmpl_id, base, sequence, compute_price, percent_price, min_quantity, pricelist_id) VALUES ('1_product', " +str(i.id)+ ", 'list_price', 0, 'percentage', " + str( self.Descuento)+ ", 1, " +str(self.Tarifa.id)+ "); ")
        return {}
