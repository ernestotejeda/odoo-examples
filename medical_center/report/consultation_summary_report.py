# Copyright 2023 MiEmpresa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ReportMedicalConsultation(models.AbstractModel):
    _name = "report.report_medical_consultation"
    _description = "Proforma Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["medical.consultation"].browse(docids)
        return {
            "doc_ids": docs.ids,
            "doc_model": "medical.consultation",
            "docs": docs,
            "custom_parameter": "Custom parameter",
        }
