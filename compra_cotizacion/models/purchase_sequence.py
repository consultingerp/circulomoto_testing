# -*- coding: utf-8 -*-

from odoo import fields, models, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sequence_ref = fields.Integer('No.', compute="_sequence_ref")

    @api.depends('order_id.order_line', 'order_id.order_line.product_id')
    def _sequence_ref(self):
        for line in self:
            no = 0
            for l in line.order_id.order_line:
                no += 1
                l.sequence_ref = no
    