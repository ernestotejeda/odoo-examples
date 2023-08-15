# Copyright 2023 MiEmpresa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    config = env["res.config.settings"].create({"group_product_variant": True})

    # *** NO FUNCIONA, no se por qué
    config.sudo().execute()
