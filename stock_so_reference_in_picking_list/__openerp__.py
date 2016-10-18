{
    'name': "Set Sales Order customer reference in Picking List",
    'version': '9.0.1.0.0',
    'depends': ['sale', 'stock'],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Stock',
    'description': 
    """
This modules adds a field on the Picking List that is a copy of the content
of the custumer reference in the Sales Order that created the Picking list.

This module has been developed by Valentin THIRION @ AbAKUS it-solutions.
    """,
    'data': [
        'views/stock_picking_view.xml',
    ],
}