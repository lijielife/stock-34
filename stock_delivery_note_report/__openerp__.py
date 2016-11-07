{
    'name': "Stock Delivery Note",
    'version': '9.0.1.0.1',
    'depends': ['stock',],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Warehouse',
    'description': """
Stock delivery report

This modules creates a report for deliveries that will be exported and printed for the customer.
It shows the current delivery, the waiting lines for the delivery and all the other lines waiting for the customer.

This module has been developed by Valentin THIRION @ AbAKUS it-solutions.
""",
    'data': [
        'reports/stock_delivery_report.xml',
        'views/delivery_note.xml',
             ],
}
