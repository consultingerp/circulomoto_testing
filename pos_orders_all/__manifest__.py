# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "All in One POS Features",
    "version" : "11.0.0.1",
    "category" : "Point of Sale",
    "depends" : ['base','sale','point_of_sale'],
    "author": "BrowseInfo",
    'summary': 'All in One POS feature POS All Orders List, POS Reorder, POS Order Reprint, POS Coupons Discount & Gift Vouchers, POS Bag Charges, POS Order Return, POS Sale order, POS Invoice Auto Check, POS Stock, POS Items Count, POS fixed amount discount,  Filter Orders based on Customers',
    "description": """

    Purpose :-
    All in One - POS All Orders List, POS Reorder, POS Order Reprint, POS Coupons Discount & Gift Vouchers, POS Bag Charges, POS Order Return - POS Return Products, POS Sale order- Create Sales from POS, POS Invoice Auto Check, POS Stock, Filter Orders based on Customers.
    All in One - Point of Sale All Orders List, Point of Sale Reorder, Point of Sale Order Reprint, POS Coupons Discount & Gift Vouchers, POS Bag Charges, Point of Sale Order Return, Point of Sale create Sale order, Point of Sale Invoice Auto Check, Point of Sale Stock,Point of Sale Filter Orders based on Customers, Display Total Number of Purchased Items in Cart and POS Receipt, Add fixed amount discount option along with percentage, 
    """,
    "website" : "www.browseinfo.in",
    "price": 89,
    "currency": 'EUR',
    "data": [
        'security/ir.model.access.csv',
        'views/custom_pos_view.xml',
        'data/data.xml',
        'views/gift_coupon_report.xml',
        'views/pos_gift_coupon.xml',
        'views/pos_gift_voucher_setting.xml',
        'views/pos_order_view.xml',
        'views/report_pos_gift_coupon.xml',
        'views/pos_custom_discount_view.xml',
    ],
    'qweb': [
        'static/src/xml/pos_orders_all.xml',
    ],
    "auto_install": False,
    "installable": True,
    "images":['static/description/Banner.png'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
