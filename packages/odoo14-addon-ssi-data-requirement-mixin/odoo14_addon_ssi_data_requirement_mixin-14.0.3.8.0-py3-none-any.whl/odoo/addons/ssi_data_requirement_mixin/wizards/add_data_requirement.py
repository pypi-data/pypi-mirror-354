# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import date as datetime_date

from odoo import api, fields, models


class AddDataRequirement(models.TransientModel):
    _name = "add_data_requirement"
    _description = "Add Data Requirement"

    @api.model
    def _default_model_id(self):
        result = False
        model_name = self.env.context.get("active_model", False)
        if model_name:
            obj_model = self.env["ir.model"]
            criteria = [
                ("model", "=", model_name),
            ]
            models = obj_model.search(criteria)
            if len(models) > 0:
                result = models[0]

        return result

    @api.model
    def _default_res_id(self):
        return self.env.context.get("active_id", 0)

    model_id = fields.Many2one(
        string="Model",
        comodel_name="ir.model",
        required=True,
        default=lambda self: self._default_model_id(),
    )
    res_id = fields.Integer(
        string="Res ID",
        required=True,
        default=lambda self: self._default_res_id(),
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="data_requirement_type_category",
        required=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="data_requirement_type",
        required=True,
    )

    @api.onchange(
        "category_id",
    )
    def onchange_type_id(self):
        self.type_id = False

    def action_confirm(self):
        for record in self:
            result = record._confirm_wizard()
        return result

    def _confirm_wizard(self):
        self.ensure_one()
        data_requirement = self._create_data_requirement()
        waction = self.env.ref(
            "ssi_data_requirement_mixin.data_requirement_action"
        ).read()[0]
        waction = {
            "name": "Data Requirement",
            "type": "ir.actions.act_window",
            "res_model": "data_requirement",
            "view_mode": "form",
            "res_id": data_requirement.id,
            "view_id": self.env.ref(
                "ssi_data_requirement_mixin.data_requirement_view_form"
            ).id,
            "target": "current",
        }
        return waction

    def _prepare_data_requirement(self):
        self.ensure_one()
        mixin = self.env[self.model_id.model].browse([self.res_id])[0]
        commercial_partner = getattr(mixin, mixin._data_requirement_partner_field_name)
        contact = getattr(mixin, mixin._data_requirement_contact_field_name)
        if self.type_id.duration_id:
            date_commitment = self.type_id.duration_id.get_duration(
                datetime_date.today()
            )
        else:
            date_commitment = datetime_date.today()
        return {
            "partner_id": commercial_partner.id,
            "contact_partner_id": contact.id,
            "type_id": self.type_id.id,
            "date": datetime_date.today(),
            "date_commitment": date_commitment,
            "mode": self.type_id.mode,
            "title": self.type_id.name,
        }

    def _create_data_requirement(self):
        self.ensure_one()
        data = self._prepare_data_requirement()
        DR = self.env["data_requirement"]
        data_requirement = DR.create(data)
        data_requirement.onchange_data_text()
        mixin = self.env[self.model_id.model].browse([self.res_id])[0]
        mixin.write(
            {
                "data_requirement_ids": [(4, data_requirement.id)],
            }
        )
        return data_requirement
