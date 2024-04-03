{
    'name': 'odoo_learn',
    'version': '1.0',
    'summary': 'Odoo Learn',
    'description': 'Odoo Learn',
    'category': 'OTHER',
    'author': 'Test',
    'depends': [],
    'sequence': 1,
    'data': [
        'security/Security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/wizard_reason_view.xml',
        'views/department_view.xml',
        'views/company_view.xml',
        'views/modern_views.xml',
    ],
    # 'installable': True,
    # 'auto_install': False
    'application': True,
}
