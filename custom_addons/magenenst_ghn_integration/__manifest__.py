{
    'name': "GHN ",
    'summary': """Integration App In Odoo With Delivery In Company GHN""",
    # 'description': """ ghn API """,
    'sequence':'10',
    'category': 'Extra Tools',
    'version': '1.0',
    'depends': ['base','contacts', 'sale', 'delivery', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'data/ghn_cron_job.xml',
        # 'wizard/create_appointment.xml',
        # 'views/patient.xml',
        'views/res_partner.xml',
        'views/delivery_carrier.xml',
        'views/res_company.xml',
        'views/sale_order_view.xml',
        'views/res_state_district_view.xml',
        'views/res_ward_view.xml',
        'views/stock_picking.xml',
        'views/res_config_settings_view.xml',
        'views/stock_warehouse.xml',
        'views/res_country_state.xml',
        'views/lunch_call_api.xml',
        # 'reports/appointment.xml',
        'wizard/choose_delivery_carrier_view.xml',

    ],
    'demo': [],
    'qweb': [],
    'auto_install': False, # this module will automatically be installed if all of its dependencies are installed
    'installable': True,
    'application': True, # application or technical module
    'auto_install': False,

}