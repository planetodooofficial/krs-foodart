{
    'name': 'Kairos Food Art',
    'version': '2.0',
    'category': 'Hidden',
    'sequence': 10,
    'summary': 'FoodArt',
    'depends': ['base', 'purchase', 'account', 'sale', 'product', 'project', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/Contacts_Import_View.xml',
        'wizard/Sale_order_import_view.xml',
        'wizard/purchase_order_import_view.xml',
        'views/product_inherit.xml',
        'views/sale_inherit.xml',
        'views/self_billing.xml',
        'views/hr_expense_inherit.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}