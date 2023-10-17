# Copyright 2023 MiEmpresa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestMedicalCenterSale(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        cls.product_category = cls.env["product.category"].create(
            {
                "name": "Test Category",
            }
        )
        cls.test_product_delivery = cls.env["product.product"].create(
            {
                "name": "Product A",
                "type": "product",
                "taxes_id": [(5, 0, 0)],
                "supplier_taxes_id": [(5, 0, 0)],
                "lst_price": 100.0,
                "standard_price": 10.0,
                "invoice_policy": "delivery",
                "property_account_income_id": cls.company_data[
                    "default_account_revenue"
                ].id,
                "property_account_expense_id": cls.company_data[
                    "default_account_expense"
                ].id,
            }
        )
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.test_product_delivery.id,
                            "product_uom_qty": 10,
                        }
                    ),
                ],
            }
        )

    def test_sale_pick_inv_flow(self):
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.order_line.qty_delivered, 0)
        self.assertEqual(self.sale_order.order_line.qty_to_invoice, 0)
        self.assertEqual(self.sale_order.order_line.qty_invoiced, 0)
        picking = self.sale_order.picking_ids
        picking.move_ids.quantity_done = 10
        picking.button_validate()
        self.assertTrue(picking.state, "done")
        self.assertEqual(self.sale_order.order_line.qty_delivered, 10)
        self.assertEqual(self.sale_order.order_line.qty_to_invoice, 10)
        self.assertEqual(self.sale_order.order_line.qty_invoiced, 0)
        # Let's do an invoice with invoiceable lines
        payment = (
            self.env["sale.advance.payment.inv"]
            .with_context(
                active_model="sale.order",
                active_ids=[self.sale_order.id],
                active_id=self.sale_order.id,
                default_journal_id=self.company_data["default_journal_sale"].id,
            )
            .create({"advance_payment_method": "delivered"})
        )
        payment.create_invoices()
        invoice = self.sale_order.invoice_ids[0]
        self.assertEqual(
            invoice.invoice_line_ids.quantity, self.sale_order.order_line.qty_delivered
        )
        self.assertEqual(self.sale_order.order_line.qty_delivered, 10)
        self.assertEqual(self.sale_order.order_line.qty_to_invoice, 0)
        self.assertEqual(self.sale_order.order_line.qty_invoiced, 10)
        invoice.action_post()
