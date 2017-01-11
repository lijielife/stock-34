{
    'name': "Stock Auto actions",
    'version': '9.0.1.0',
    'depends': ['stock'],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Stock',
    'description': 
    """
This modules adds auto actions for managing Delivery Orders
- every 30 minutes:
    - it checks availability for pickings that are waiting
    - it prints the ready pickings and set them as printed
    """,
    'data': ['delivery_order_cron.xml', 'view/stock_picking_view.xml',],
}
