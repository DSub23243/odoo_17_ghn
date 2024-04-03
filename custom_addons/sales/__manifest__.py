{
    'name': 'Sales diary',
    'version': '1.0.0',
    'summary': 'Sales diary',
    'description': 'Sales diary',
    'category': 'Other',
    'author': 'Author',
    'depends': [
        'account',
        'base',
        'sale',
        'payment',
        'payment_demo',
    ],
    'data': [
        'security/secutity.xml',
        'security/ir.model.access.csv',
        'views/diary_order_view.xml',
        'views/auto_invoices.xml',
        'views/payment_demo.xml',
        'views/order_invoice.xml',

        'report/sales_template.xml',
        'report/sales_invoice_template.xml',
    ],
        # 'assets': {
        #   'web.assets_backend': [
        #         'sales/static/src/js/custom_notification.js'
        #   ],
        # },
    'application': True
    # 'installable': True,
    # 'auto_install': False
}
