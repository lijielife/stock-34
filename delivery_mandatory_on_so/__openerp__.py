{
    'name': "Delivery method mandatory on SO",
    'version': '9.0.1.0.1',
    'depends': ['delivery', 'sale'],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Sale',
    'description': """
It simply makes the field 'delivery method' mandatory on Sales Order

This module has been developed by Valentin THIRION @ AbAKUS it-solutions""",
    'data': [
        'views/sale_order_views.xml',
    ],
}