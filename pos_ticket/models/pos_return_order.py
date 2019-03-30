# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _

class posOrderReturn(models.Model):
	_inherit = 'pos.order'

	invisible_refund = fields.Boolean(string='Retorno',default=False,readonly=True)
	
	@api.multi
	def refund(self):
		"""Create a copy of order  for refund order"""
		PosOrder = self.env['pos.order']
		self.invisible_refund = True
		current_session = self.env['pos.session'].search([('state', '!=', 'closed'), ('user_id', '=', self.env.uid)], limit=1)
		if not current_session:
			raise UserError(_('To return product(s), you need to open a session that will be used to register the refund.'))
		for order in self:
			clone = order.copy({
				# ot used, name forced by create
				'name': order.name + _(' REFUND'),
				'session_id': current_session.id,
				'date_order': fields.Datetime.now(),
				'pos_reference': order.pos_reference,
				'lines': False,
			})
			for line in order.lines:
				clone_line = line.copy({
					# required=True, copy=False
					'name': line.name + _(' REFUND'),
					'order_id': clone.id,
					'qty': -line.qty,
				})
			PosOrder += clone
			print('pos order ',PosOrder)
		#return {
			#'name': _('Return Products'),
			#'view_type': 'form',
			#'view_mode': 'form',
			#'res_model': 'pos.order',
			#'res_id': PosOrder.ids[0],
			#'view_id': False,
			#'context': self.env.context,
			#'type': 'ir.actions.act_window',
			#'target': 'current',
		#}