# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class MedicalConsultation(models.Model):
    _name = "medical.consultation.report"
    _description = "Medical Consultation Report"
    _auto = False
    _rec_name = "date"
    _order = "date desc"

    name = fields.Char("Order Reference", readonly=True)
    date = fields.Datetime("Order Date", readonly=True)
    product_id = fields.Many2one("product.product", "Product Variant", readonly=True)
    product_uom_id = fields.Many2one("uom.uom", "Unit of Measure", readonly=True)
    product_qty = fields.Float("Qty Ordered", readonly=True)
    partner_id = fields.Many2one("res.partner", "Customer", readonly=True)
    company_id = fields.Many2one("res.company", "Company", readonly=True)
    country_id = fields.Many2one("res.country", "Customer Country", readonly=True)
    consultation_id = fields.Many2one("sale.order", "Order #", readonly=True)
    nbr = fields.Integer("# of Lines", readonly=True)
    categ_id = fields.Many2one("product.category", "Product Category", readonly=True)
    product_tmpl_id = fields.Many2one("product.template", "Product", readonly=True)
    commercial_partner_id = fields.Many2one(
        "res.partner", "Customer Entity", readonly=True
    )

    def _select_sale(self, fields=None):
        if not fields:
            fields = {}
        select_ = """
            min(l.id) as id,
            l.product_id as product_id,
            t.uom_id as product_uom_id,
            CASE
                WHEN l.product_id IS NOT NULL
                    THEN sum(l.product_qty / u.factor * u2.factor)
                ELSE
                    0
            END as product_qty,
            count(*) as nbr,
            s.name as name,
            s.date_consultation as date,
            s.partner_id as partner_id,
            s.company_id as company_id,
            t.categ_id as categ_id,
            p.product_tmpl_id,
            partner.country_id as country_id,
            partner.commercial_partner_id as commercial_partner_id,
            s.id as consultation_id
        """

        for field in fields.values():
            select_ += field
        return select_

    def _from_sale(self, from_clause=""):
        from_ = (
            """
                medication_administer l
                      left join medical_consultation s on (s.id=l.consultation_id)
                      join res_partner partner on s.partner_id = partner.id
                        left join product_product p on (l.product_id=p.id)
                            left join product_template t on (p.product_tmpl_id=t.id)
                    left join uom_uom u on (u.id=l.product_uom_id)
                    left join uom_uom u2 on (u2.id=t.uom_id)
                %s
        """
            % from_clause
        )
        return from_

    def _group_by_sale(self, groupby=""):
        groupby_ = """
            l.product_id,
            t.uom_id,
            s.name,
            s.date_consultation,
            s.partner_id,
            s.company_id,
            t.categ_id,
            p.product_tmpl_id,
            partner.country_id,
            partner.commercial_partner_id,
            s.id %s
        """ % (
            groupby
        )
        return groupby_

    def _query(self, with_clause="", fields=None, groupby="", from_clause=""):
        if not fields:
            fields = {}
        sale_report_fields = fields
        with_ = ("WITH %s" % with_clause) if with_clause else ""
        return "%s (SELECT %s FROM %s WHERE l.display_type IS NULL GROUP BY %s)" % (
            with_,
            self._select_sale(sale_report_fields),
            self._from_sale(from_clause),
            self._group_by_sale(groupby),
        )

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query())
        )
