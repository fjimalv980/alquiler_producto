{
    'name': 'Alquiler de Productos',
    'version': '1.0',
    'author': 'Francisco Jiménez',
    'category': 'Sales',
    'summary': 'Gestión de Alquiler de Productos',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/alquiler_producto_views.xml',
    ],
    'icon': '/alquiler_producto/static/description/icon.png',
    'installable': True,
    'application': True,
}