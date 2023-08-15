# Copyright 2023 MiEmpresa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Medical Center",
    "version": "15.0.1.0.0",
    "summary": "Medical center managements",
    "category": "health",
    "author": "Ernesto Tejeda",
    "website": "https://github.com/ernestotejeda/odoo-examples",
    "license": "AGPL-3",
    "depends": [
        "sale_stock",
        "purchase",
        "project",
        "hr",
        "l10n_generic_coa",
    ],
    "data": [
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv",
        "views/menus.xml",
        "views/res_partner_views.xml",
        "views/product_views.xml",
        "views/medical_consultation_views.xml",
        "report/consultation_report_views.xml",
        "report/consultation_summary_report.xml",
        "report/consultation_report.xml",
    ],
    "application": True,
    "post_init_hook": "post_init_hook",
}
