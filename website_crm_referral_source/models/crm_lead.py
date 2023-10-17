# Copyright 2023 MiEmpresa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    referral_source = fields.Selection(
        [
            ("third_party", "Third Party"),
            ("social_network", "Social Network"),
            ("internet_searching", "Internet Searching"),
        ]
    )
