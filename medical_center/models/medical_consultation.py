# Copyright 2023 MiEmpresa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MedicalConsultation(models.Model):
    _name = "medical.consultation"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Medical Consultation"

    name = fields.Char(
        string="Order Reference",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Patient",
        # readonly=True,
        # states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True,
        change_default=True,
        index=True,
        tracking=1,
        domain="[('is_patient', '=', True), ('company_id', 'in', (False, company_id))]",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )
    date_consultation = fields.Datetime()
    symptoms = fields.Html()
    diagnosis = fields.Html()
    medication_administer_ids = fields.One2many(
        comodel_name="medication.administer",
        inverse_name="consultation_id",
    )

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            seq_date = None
            if "date_order" in vals:
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals["date_consultation"])
                )
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "medical.consultation", sequence_date=seq_date
            ) or _("New")
        return super().create(vals)


class MedicationAdminister(models.Model):
    _name = "medication.administer"
    _description = "Medication Administer"

    name = fields.Char()
    sequence = fields.Integer(default=10)
    product_id = fields.Many2one(
        "product.product", string="Medicine", domain="[('is_medicine', '=', True)]"
    )
    product_qty = fields.Float(string="Dose")
    product_uom_id = fields.Many2one(
        "uom.uom",
        domain="[('category_id', '=', product_uom_category_id)]",
        ondelete="restrict",
    )
    product_uom_category_id = fields.Many2one(related="product_id.uom_id.category_id")
    route = fields.Selection(
        [
            ("injection", "Injection"),
            ("oral", "Oral"),
        ]
    )
    consultation_id = fields.Many2one(comodel_name="medical.consultation")
    company_id = fields.Many2one(
        comodel_name="res.company", related="consultation_id.company_id"
    )
    display_type = fields.Selection(
        selection=[("line_section", "Section"), ("line_note", "Note")],
        default=False,
        help="Technical field for UX purpose.",
    )

    @api.onchange("product_id")
    def on_change_product_id(self):
        self.name = self.product_id.display_name
