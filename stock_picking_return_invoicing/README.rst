.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================
Refund Returned Pickings from Sales and Purchase Orders
==========================================

This module extends the functionality of sales and purchase orders to
support marking some returned pickings as "To refund in Order" and
to allow you to create invoices deducting the products that are
returned and refunded.

Usage
=====

To use this module, when some customer returns some refundable products to you
before you created an invoice, you need to:

#. Go to *Sales > Sales Orders > Create*.
#. Choose a customer and add a product whose *Invoicing Policy* is *Delivered
   quantities*, and input some quantity to sell.
#. Confirm the sale.
#. Go to *Delivery > Validate > Apply > Reverse*.
#. Set *Quantity* to a lower quantity than the sold one, and enable
   *To Refund*.
#. Press *Return > Validate > Apply*.
#. Go back to the sale order.
#. Press *Create Invoice > Invoiceable lines > Create and View Invoices*.
#. The created invoice's amount will be the difference between the delivered
   and the returned quantity.

To use this module, when some customer returns some refundable products to you
after you created an invoice, you need to:

#. Go to *Sales > Sales Orders > Create*.
#. Choose a customer and add a product whose *Invoicing Policy* is *Delivered
   quantities*, and input some quantity to sell.
#. Confirm the sale.
#. Go to *Delivery > Validate > Apply*.
#. Return to the sale order.
#. Press *Create Invoice > Invoiceable lines > Create and View Invoices*.
#. The created invoice's amount is the same you sold.
#. Return to the sale order.
#. Go to *Delivery > Reverse*.
#. Set *Quantity* to a lower quantity than the sold one, and enable
   *To Refund*.
#. Press *Return > Validate > Apply*.
#. Return to the sale order.
#. Press *Create Invoice > Invoiceable lines (deduct down payments) >
   Create and View Invoices*.
#. A refund is created for the quantity you returned before.

#. The behaviour is exactly the same for Purchase Orders

Known issues / Roadmap
======================

* This addon is a pseudobackport of a functionality that exists natively in
  v10, plus a fix for https://github.com/odoo/odoo/issues/13974, so this addon
  will never have to be migrated to v10.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Jairo Llopis <jairo.llopis@tecnativa.com>
* Valentin Thirion <vt@abakus.be>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
