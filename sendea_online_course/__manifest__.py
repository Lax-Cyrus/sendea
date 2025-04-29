{
    'name': 'Online Course Application Form',
    'version': '1.0',
    'summary': 'Collects applications for online courses',
    'category': 'Website',
    'author': 'Your Company',
    'depends': ['portal', 'website'],
    'data': [
        'views/application_form_template.xml',
        'views/application_form_menus.xml',
        'views/application_form_views.xml',
        'security/ir.model.access.csv',
        'data/email_data.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         'sendea_online_course/static/src/js/application_form.js',
    #     ],
    # },
    'installable': True,
    'auto_install': False,
    'website': '#',
    'license': 'LGPL-3',
    'application': True,
}
