# Copyright 2023 MiEmpresa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, Form
from odoo.exceptions import UserError


class TestSaleOrderRestrictZeroQuantities(TransactionCase):
    def setUp(self):
        super().setUp()
        partner = self.env["res.partner"].create({"name": "Partner Test"})
        product1 = self.env["product.product"].create({"name": "Product Test 1"})
        product2 = self.env["product.product"].create({"name": "Product Test 2"})
        product3 = self.env["product.product"].create({"name": "Product Test 3"})
        product4 = self.env["product.product"].create({"name": "Product Test 4"})
        sale_form = Form(self.env["sale.order"])
        sale_form.partner_id = partner
        with sale_form.order_line.new() as line_form:
            line_form.product_id = product1
            line_form.product_uom_qty = 3
        with sale_form.order_line.new() as line_form:
            line_form.product_id = product2
            line_form.product_uom_qty = 0
        with sale_form.order_line.new() as line_form:
            line_form.product_id = product3
            line_form.product_uom_qty = 2
        with sale_form.order_line.new() as line_form:
            line_form.product_id = product4
            line_form.product_uom_qty = 0

        self.sale_order = sale_form.save()

    def test_confirm_sale_order(self):
        with self.assertRaises(UserError):
            self.sale_order.action_confirm()

    def test_remove_lines_at_zero(self):
        self.sale_order.action_remove_at_zero()
        sale_order_state = self.sale_order.state
        self.sale_order.action_confirm()
        self.assertNotEqual(self.sale_order.state, sale_order_state)


