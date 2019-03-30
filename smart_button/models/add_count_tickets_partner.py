# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Add_comercial_name(models.Model):
    _inherit = 'res.partner'

    x_blemer_ticket_count = fields.Integer(
        string='Tickets',
        compute='compute_tickets_count'
    )
    #default=lambda self: self.env['helpdesk.ticket'].search_count([('partner_id', '=', self.id)]),

    @api.multi
    def compute_tickets_count(self):
        for partner in self:
            partner.x_blemer_ticket_count = self.env['helpdesk.ticket'].search_count(
                [('partner_id', '=', partner.id)])
