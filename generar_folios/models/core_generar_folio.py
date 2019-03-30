# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api
"""
@miguel.cabrera

"""
class CoreGeneradorFolios(models.Model):
    _name = 'core_generador_folio';
    nombre_folio = fields.Char(string='Nombre del folio', required=True)
    prefijo = fields.Char(string='Prefijo', required=True,
                          help='Se se usará como parte fundamental en el folio generado')
    contador = fields.Integer(default=0)
    incrementar = fields.Integer(default=lambda self: 1)
    numero_zeros = fields.Integer(string='Número de ceros a la izquierda', default=0)
    formato_fecha = fields.Char(string='Ingrese el formato de la fecha si lo requiere',
                                help='Por ejemplo: %Y-%m-%d o %Y%m%d%H%%i%s')
    
    tipo_folio_id = fields.Many2one(
        'core_formato_folio',
        string='Formato del folio',
        inverse_name='formato',
        ondelete='set null'
    )

    # agregar el constrain de prefijo unico

    @api.multi
    def getFolio(self, par_prefijo_folio):
        coreFolio = self.env['core_generador_folio'].search([('prefijo','=', par_prefijo_folio)])
        folio = ""
        if coreFolio:
            contador_actual = coreFolio.contador + coreFolio.incrementar
            folio = self.crearFolioByFormato(coreFolio.tipo_folio_id.formato, coreFolio, contador_actual)
            coreFolio.write({'contador': contador_actual})
        return folio

    def crearFolioByFormato(self, par_formato, par_campos, contador_actual):
        folio_final = str(par_formato)
        fields_search = [
            'prefijo',
            'numero_zeros',
            'contador',
            'formato_fecha'
        ]
        for val in fields_search:
            if val in par_campos:
                key = par_campos[val]
                if val == 'contador':
                    key = str(contador_actual).zfill(par_campos.numero_zeros)
                elif val == 'formato_fecha' and key:
                    key = str(datetime.datetime.now().strftime(key))
                key = str(key)
                folio_final = folio_final.replace('{' + val + '}', key)
        return folio_final;

    def createGenericFolio(self, data):
        self.create(data)
        # print (data)
        return self.getFolio(data['prefijo'])
