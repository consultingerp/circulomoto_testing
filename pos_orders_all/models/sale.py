# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from openerp import fields, models, api, _, tools
import logging
_logger = logging.getLogger(__name__)


class PosConfiguration(models.Model):
    _inherit = 'pos.config'
    
    discount_type = fields.Selection([('percentage', "Percentage"), ('fixed', "Fixed")], string='Discount Type', default='percentage', help='Seller can apply different Discount Type in POS.')
    


class pos_order(models.Model):
    _inherit = 'pos.order'

    coupon_id = fields.Many2one('pos.gift.coupon')
    discount_type = fields.Char(string='Discount Type')

    @api.model
    def create_from_ui(self, orders):
        order_ids = super(pos_order, self).create_from_ui(orders)
        for order_id in order_ids:
            try:
                pos_order_id = self.browse(order_id)
                if pos_order_id:
                    ref_order = [o['data'] for o in orders if o['data'].get('name') == pos_order_id.pos_reference]
                    for order in ref_order:
                        if pos_order_id.session_id.config_id.discount_type == 'percentage':
                            pos_order_id.update({'discount_type': "Percentage"})
                        if pos_order_id.session_id.config_id.discount_type == 'fixed':
                            pos_order_id.update({'discount_type': "Fixed"})
                        coupon_id = order.get('coupon_id', False)
                        pos_order_id.write({'coupon_id':  coupon_id})
                        pos_order_id.coupon_id.update({'coupon_count': pos_order_id.coupon_id.coupon_count + 1})
            except Exception as e:
                _logger.error('Error in point of sale validation: %s', tools.ustr(e))
        return order_ids


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
