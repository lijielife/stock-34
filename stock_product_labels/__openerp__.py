# This code has been written
# by AbAKUS it-solutions PGmbH
# in Belgium, 2015

{
    'name': "Product Stock Labels",
    'version': '9.0.1.0',
    'depends': ['stock', 'sale', 'product_brand'],
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'summary': 'Stocked product Labels',
    'category': 'Warehouse',
    'description': """
This modules adds a report on the products in order to print a label for each stocked (available stock > 0) product.

This module has been developped by Valentin THIRION @ AbAKUS it-solutions
    """,
    'data': [
    		'report/product_stock_label.xml',
            'view/product_labels_view.xml',
    		],
}
