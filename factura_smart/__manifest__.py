{
    'name' : "Cambiar la informacion de la generacion de la FACTURA(PDF)",
    'version' : "1.0",
    'description' : "FACTURA CFDI 3.3",
    'author' : "Soluciones4g", 
    'depends' : ['l10n_mx_edi','web','account'],
    'data': [
    	'views/l10n_mx_edi_report_invoice_document_mx.xml',
    	'views/web_external_layout_background.xml',
    	'views/invoice_cancel_watermark.xml',
        'views/account_payment_complement.xml'
    ],
    'installable' : True,
}
