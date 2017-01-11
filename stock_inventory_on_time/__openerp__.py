# -*- encoding: utf-8 -*-
# This code has been written
# by AbAKUS it-solutions PGmbH
# in Belgium, 2015

{
    'name': 'Stock Inventory On Time Report',
    'version': '8.0.1.0',
    'license': 'AGPL-3',
    'author': "AbAKUS it-solutions",
    'category': 'Warehouse',
    'website': 'http://www.abakusitsolutions.eu',
    'summary': 'Period Inventory Report',
    'sequence': 20,
    'description': """
Stock Inventory on Time
======================

This modules creates a new PDF report for Inventory selected for a certain time period.

A new menuitem appears in the warehouse menu that allows to select a peride (between 2 dates) and a stock location.
The system will put in the file all the products that stocked during this period.

This model has been developped by Valentin THIRION @ AbAKUS it-solutions

SQL credit: https://github.com/quanvm00/Inventory-Report
    """,
    'depends': ['stock'],
    'data': [
        'wizard/stock_inventory_report_wizard.xml',
        'report/stock_inventory_report_report.xml',
    ],
    'installable': True,
}
