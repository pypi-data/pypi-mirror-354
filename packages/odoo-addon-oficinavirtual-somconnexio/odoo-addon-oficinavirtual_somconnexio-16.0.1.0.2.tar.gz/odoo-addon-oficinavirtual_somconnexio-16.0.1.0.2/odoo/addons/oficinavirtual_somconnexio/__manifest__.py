{
    "name": "oficinavirtual_somconnexio",
    "version": "16.0.1.0.2",
    "summary": """
        Integrates office virtual functionalities specific to Som Connexió.
    """,
    "author": "Som Connexió SCCL, Coopdevs Treball SCCL",
    "website": "https://git.coopdevs.org/coopdevs/som-connexio/odoo/odoo-somconnexio",
    "category": "Cooperative Management",
    "license": "AGPL-3",
    "depends": ["res_partner_api_somconnexio"],
    "data": [
        "wizards/partner_check_somoffice_email/partner_check_somoffice_email.xml",
        "data/ir_config_pararameter.xml",
    ],
    "demo": [],
    "external_dependencies": {},
    "application": False,
    "installable": True,
}
