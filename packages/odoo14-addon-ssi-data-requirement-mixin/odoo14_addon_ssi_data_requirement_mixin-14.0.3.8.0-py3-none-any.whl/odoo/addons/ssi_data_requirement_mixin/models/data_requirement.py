# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class DataRequirement(models.Model):
    _name = "data_requirement"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.localdict",
        "mixin.partner",
    ]
    _description = "Data Requirement"

    # Multiple Approval Attribute
    _approval_from_state = "open"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    # mixin.partner configuration
    _mixin_partner_insert_form = True
    _mixin_partner_insert_tree = True
    _mixin_partner_insert_search = True
    _mixin_partner_contact_id_required = True

    _statusbar_visible_label = "draft,open,confirm"
    _policy_field_order = [
        "open_ok",
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    package_id = fields.Many2one(
        string="# Data Requirement Package",
        comodel_name="data_requirement_package",
        readonly=True,
        ondelete="restrict",
    )
    date = fields.Date(
        string="Date",
        default=lambda self: self._default_date(),
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    duration_id = fields.Many2one(
        string="Duration",
        comodel_name="base.duration",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_commitment = fields.Date(
        string="Commitment Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date_submit = fields.Date(
        string="Submit Date",
        required=False,
        readonly=True,
        states={"open": [("readonly", False)]},
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="data_requirement_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    title = fields.Char(
        string="Title",
        default="-",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    category_id = fields.Many2one(
        string="Category",
        related="type_id.category_id",
        store=True,
    )
    mode = fields.Selection(
        string="Mode",
        selection=[
            ("url", "URL"),
            ("attachment", "Attachment"),
            ("text", "Free Text"),
        ],
        required=True,
        readonly=True,
        default="url",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    data_text = fields.Text(
        string="Data",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "open": [
                ("readonly", False),
            ],
        },
    )
    url = fields.Char(
        string="URL",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "open": [
                ("readonly", False),
            ],
        },
    )
    attachment_id = fields.Many2one(
        string="Attachment",
        comodel_name="ir.attachment",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "open": [
                ("readonly", False),
            ],
        },
    )
    instruction_url = fields.Char(
        string="Instruction URL",
    )

    @api.model
    def _default_date(self):
        return fields.Date.today()

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "open_ok",
            "confirm_ok",
            "approve_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange(
        "type_id",
    )
    def onchange_duration_id(self):
        self.duration_id = False
        if self.type_id:
            self.duration_id = self.type_id.duration_id

    @api.onchange(
        "duration_id",
        "date",
    )
    def onchange_date_commitment(self):
        self.date_commitment = False
        if self.duration_id:
            self.date_commitment = self.duration_id.get_duration(self.date)

    @api.onchange(
        "type_id",
    )
    def onchange_title(self):
        self.title = False
        if self.type_id:
            self.title = self.type_id.name

    @api.onchange(
        "type_id",
    )
    def onchange_instruction_url(self):
        self.instruction_url = False
        if self.type_id.instruction_url:
            self.instruction_url = self.type_id.instruction_url

    @api.onchange(
        "mode",
    )
    def onchange_data_text(self):
        self.data_text = ""
        if self.type_id.text_template:
            self.data_text = self.type_id.text_template

    @ssi_decorator.post_done_action()
    def _update_date_submit(self):
        self.ensure_one()
        if not self.date_submit:
            self.write(
                {
                    "date_submit": fields.Date.today(),
                }
            )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
