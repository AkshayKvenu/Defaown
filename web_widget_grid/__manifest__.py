
{
    "name": "Web Widget grid",
    "category": "Hidden",
    "summary": "",
    "author": "",
    "version": "11.0.1.1.0",
    "website": "",
    'depends': ['base', 'web','mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/web_widget_color_view.xml',
        'views/views.xml'
    ],
    'qweb': [
        'static/src/xml/widget.xml',
    ],
    "auto_install": False,
}
