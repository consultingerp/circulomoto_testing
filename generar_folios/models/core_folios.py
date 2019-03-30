# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CoreFolios(models.Model):
    _name = 'core_formato_folio'

    formato = fields.Char(required=True)

    @api.multi
    def name_get(self):
        # result = super(self.env['op.faculty'], self).name_get()
        res = []
        for element in self:
            name = ''
            name += element.formato or ''
            res.append((element.id, name))
        return res
