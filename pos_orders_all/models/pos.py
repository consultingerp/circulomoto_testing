# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import Warning
import random
from datetime import date, datetime



class pos_create_sales_order(models.Model):
    _name = 'pos.create.sales.order'

    @api.multi
    def create_sales_order(self, partner_id, orderlines):
        # print "****************codeeeeeeeeeeeeeeeeeeeeeeeee",partner_id, orderlines
        sale_object = self.env['sale.order']
        sale_order_line_obj = self.env['sale.order.line']
        order_id = sale_object.create({'partner_id': partner_id})
        for dict_line in orderlines:
            # print "************************dict_line",dict_line
            product_obj = self.env['product.product']
            product_dict  = dict_line.get('product')
            product_name =product_obj.browse(product_dict .get('id')).name
            vals = {'product_id': product_dict.get('id'),
                    'name':product_name,
                    'customer_lead':7,
                    'product_uom_qty': product_dict.get('quantity'),
                    'price_unit':product_dict.get('price'),
                    'product_uom':product_dict.get('uom_id'),
                    'order_id': order_id.id}
            # print "-=====================================vals",vals
            sale_order_line_obj.create(vals)


        return True


class pos_order(models.Model):
    _inherit = 'pos.order'

    @api.multi
    def print_pos_report(self):
        return self.env['report'].get_action(self, 'point_of_sale.report_receipt')

    @api.multi
    def print_pos_receipt(self):
        output = []
        discount = 0
        order_id = self.search([('id', '=', self.id)], limit=1)
        orderlines = self.env['pos.order.line'].search([('order_id', '=', order_id.id)])
        payments = self.env['account.bank.statement.line'].search([('pos_statement_id', '=', order_id.id)])
        paymentlines = []
        change = 0
        for payment in payments:
            if payment.amount > 0:
                temp = {
                    'amount': payment.amount,
                    'name': payment.journal_id.name
                }
                paymentlines.append(temp)
            else:
                change += payment.amount
        for orderline in orderlines:
            new_vals = {
                'product_id': orderline.product_id.name,
                'qty': orderline.qty,
                'price_unit': orderline.price_unit,
                'discount': orderline.discount,
            }
            discount += (orderline.price_unit * orderline.qty * orderline.discount) / 100
            output.append(new_vals)

        return [output, discount, paymentlines, change]


class pos_config(models.Model):
    _inherit = 'pos.config'

    auto_check_invoice = fields.Boolean(string='Invoice Auto Check')

    pos_display_stock = fields.Boolean(string='Display Stock in POS')
    pos_stock_type = fields.Selection([('onhand', 'Qty on Hand'), ('incoming', 'Incoming Qty'), ('outgoing', 'Outgoing Qty'), ('available', 'Qty Available')], string='Stock Type', help='Seller can display Different stock type in POS.')
    pos_allow_order = fields.Boolean(string='Allow POS Order When Product is Out of Stock')
    pos_deny_order = fields.Char(string='Deny POS Order When Product Qty is goes down to')

    allow_bag_charges = fields.Boolean('Allow Bag Charges')
    pos_bag_category_id = fields.Many2one('pos.category','Bag Charges Category')

    show_stock_location = fields.Selection([
        ('all', 'All Warehouse'),
        ('specific', 'Current Session Warehouse'),
    ], string='Show Stock Of', default='all')


class stock_quant(models.Model):
    _inherit = 'stock.quant'

    @api.multi
    def get_stock_location_qty(self, location):
        res = {}
        product_ids = self.env['product.product'].search([])
        for product in product_ids:
            quants = self.env['stock.quant'].search([('product_id', '=', product.id),('location_id', '=', location['id'])])
            if len(quants) > 1:
                quantity = 0.0
                for quant in quants:
                    quantity += quant.quantity
                res.update({product.id : quantity})
            else:
                res.update({product.id : quants.quantity})
        return [res]
