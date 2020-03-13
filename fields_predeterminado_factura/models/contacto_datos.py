# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
from odoo import api
from odoo import fields
from odoo import models
# modelo de campos a editar desde factura borrados
class editable(models.Model):
    _inherit = 'res.partner'

    #asociado = fields.Many2one(related='id.bank_id')
    Banco_asociado = fields.Many2one('res.partner.bank')		
    Metodo_pago = fields.Many2one('l10n_mx_edi.payment.method')
    Transferenciaelectronica_Uso = fields.Selection(selection=[
                                                    ('G01', 'Adquisición de mercancías'), 
                                                    ('G02', 'Devoluciones, descuentos o bonificaciones'),
                                                    ('G03', 'Gastos en general'), 
                                                    ('l01', 'Construcciones'), 
                                                    ('l02', 'Mobiliario y equipo de oficina por inversiones'), 
                                                    ('l03', 'Equipo de transporte'), 
                                                    ('l04', 'Equipo de cómputo y accesorios'),
                                                    ('l05', 'Dados, troqueles, moldes, matrices y herramientas'), 
                                                    ('l06', 'Comunicaciones telefónicas'), 
                                                    ('l07', 'Comunicaciones satelitales'), 
                                                    ('l08', 'Otra maquinaria y equipo'),
                                                    ('D01', 'Honorarios médicos,dentales y gastos hospitalarios'), 
                                                    ('D02', 'Gastos médicos por incapacidad o discapacidad'), 
                                                    ('D03', 'Gastos funerales'), 
                                                    ('D04', 'Donativos'),
                                                    ('D05', 'Intereses reales efectivamente pagados'), 
                                                    ('D06', 'Aportaciones voluntarias al SAR.'), 
                                                    ('D07', 'Primas por seguros de gastos médicos'),
                                                    ('D08', 'Gastos de transportación escolar obligatoria'), 
                                                    ('D09', 'Depósitos en cuentas para el ahorro, primas que tengan como base de pensiones'),
                                                    ('D10', 'pagos de servicios educativos (colegiaturas)'), 
                                                    ('P01', 'por definir')
                                                    ],
                                                    compute='_compute_uso',
                                                    store=True, 
                                                    track_visibility='onchange',
                                                    )

    Transferencia_Uso = fields.Many2one('tranferencia.uso')
    
    @api.depends('Transferencia_Uso')
    @api.one
    def _compute_uso(self):
        if self.Transferencia_Uso.codigo == "G01":
            self.Transferenciaelectronica_Uso = "G01"
        if self.Transferencia_Uso.codigo == "G02":
            self.Transferenciaelectronica_Uso = "G02"
        if self.Transferencia_Uso.codigo == "G03":
            self.Transferenciaelectronica_Uso = "G03"
        if self.Transferencia_Uso.codigo == "l01":
            self.Transferenciaelectronica_Uso = "l01"
        if self.Transferencia_Uso.codigo == "l02":
            self.Transferenciaelectronica_Uso = "l02"
        if self.Transferencia_Uso.codigo == "l03":
            self.Transferenciaelectronica_Uso = "l03"
        if self.Transferencia_Uso.codigo == "l04":
            self.Transferenciaelectronica_Uso = "l04"
        if self.Transferencia_Uso.codigo == "l05":
            self.Transferenciaelectronica_Uso = "l05"
        if self.Transferencia_Uso.codigo == "l06":
            self.Transferenciaelectronica_Uso = "l06"
        if self.Transferencia_Uso.codigo == "l07":
            self.Transferenciaelectronica_Uso = "l07"
        if self.Transferencia_Uso.codigo == "l08":
            self.Transferenciaelectronica_Uso = "l08"
        if self.Transferencia_Uso.codigo == "D01":
            self.Transferenciaelectronica_Uso = "D01"
        if self.Transferencia_Uso.codigo == "D02":
            self.Transferenciaelectronica_Uso = "D02"
        if self.Transferencia_Uso.codigo == "D03":
            self.Transferenciaelectronica_Uso = "D03"
        if self.Transferencia_Uso.codigo == "D04":
            self.Transferenciaelectronica_Uso = "D04"
        if self.Transferencia_Uso.codigo == "D05":
            self.Transferenciaelectronica_Uso = "D05"
        if self.Transferencia_Uso.codigo == "D06":
            self.Transferenciaelectronica_Uso = "D06"
        if self.Transferencia_Uso.codigo == "D07":
            self.Transferenciaelectronica_Uso = "D07"
        if self.Transferencia_Uso.codigo == "D08":
            self.Transferenciaelectronica_Uso = "D08"
        if self.Transferencia_Uso.codigo == "D09":
            self.Transferenciaelectronica_Uso = "D09"
        if self.Transferencia_Uso.codigo == "D10":
            self.Transferenciaelectronica_Uso = "D10"
        if self.Transferencia_Uso.codigo == "P01":
            self.Transferenciaelectronica_Uso = "P01"
            
class TransferenciaUso(models.Model):
    _name = 'tranferencia.uso'
    _description = 'Version M2o de select'
    name = fields.Char(string='Opcion')
    codigo = fields.Char(string='Código')
    
