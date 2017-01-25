# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Refund Return Pickings in Sales and Purchase Orders",
    "summary": "Add an option to refund return pickings",
    "version": "9.0.2.0.0",
    "category": "Stock",
    "website": "",
    "author": "Tecnativa, AbAKUS it-solutions, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_stock",
        "purchase",
        "account_accountant",
    ],
    "data": [
        "wizards/stock_return_picking_view.xml",
        "views/purchase_order_view.xml",
    ],
}
