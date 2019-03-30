{
    'name' : "Cotizacio/Pedido Ventas",
    'version' : "1.0",
    'description' : "Personalizacion de la cotizacion/pedido de ventas directas",
    'author' : "Soluciones4g", 
    'depends' : ['sale','sale_management'],
    'data': [
    'data/ir_sequence_data.xml',
    'views/numero_partida_order_line_tree.xml',
    'views/report_sale_quotation.xml'],
    'installable' : True,
}
