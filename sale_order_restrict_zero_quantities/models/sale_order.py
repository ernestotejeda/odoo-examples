
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        if self.order_line.filtered(lambda r: not r.product_uom_qty):
            raise UserError(_('It is not allowed to confirm an order with lines at zero'))
        return super().action_confirm()

    def action_remove_at_zero(self):
        self.order_line.filtered(lambda r: not r.product_uom_qty).unlink()
