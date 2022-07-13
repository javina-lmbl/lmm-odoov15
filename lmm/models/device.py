from odoo import fields, models, api, _
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)


class Device(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'lmm.device'
    _description = 'Logica Mobile Mexico Devices model'

    name = fields.Char(
        required=True,
        string=_("GPS Device")
    )

    nick = fields.Char(
        string=_("Nick"),
    )

    imei = fields.Char(
        string=_("IMEI"),
    )

    idf = fields.Char(
        string=_("IDF"),
    )

    installation_date = fields.Date(
        string=_("Installation Date"),
    )

    warranty_start_date = fields.Date(
        string=_("Warranty Start Date"),
    )

    warranty_end_date = fields.Date(
        compute="_compute_end_warranty",
        string=_("Warranty End Date"),
        store=True,
    )

    warranty_term = fields.Selection(
        selection=[
            ("12", _("12 months")),
            ("18", _("18 months")),
            ("24", _("24 months")),
            ("36", _("36 months"))
        ],
        default="12",
        string=_("Warranty Term"),
    )
# Services that are active in this device
    tracking = fields.Boolean(
        default=False,
        string=_("Tracking"),
        tracking=True
    )

    fuel = fields.Boolean(
        default=False,
        string=_("Fuel"),
        tracking=True
    )

    temperature = fields.Boolean(
        default=False,
        string=_("Temperature"),
        tracking=True
    )

    operative_status = fields.Selection(
        selection=[
            ("drop", _("Drop")),
            ("demo", _("Demo")),
            ("uninstalled", _("Uninstalled")),
            ("installed", _("Installed")),
            ("inventory", _("Inventory")),
            ("for installing", _("For Installing")),
            ("tests", _("Tests")),
            ("rma", _("RMA")),
        ],
        default="inventory",
        string=_("Status"),
        tracking=True
    )

    platform_list_id = fields.Many2one(
        comodel_name="lmm.platforms_list",
        string=_("Platforms List"),
        ondelete="set null",
        index=True,
        domain=[('active', '=', True)],
        tracking=True,
    )

    cell_chip_id = fields.Many2one(
        comodel_name="lmm.cell_chip",
        string=_("Cell Chip Number"),
        ondelete='set null',
        required=False,
        tracking=True
    )

    product_id = fields.Many2one(
        comodel_name="product.product",
        required=True,
        string=_("Product Type"),
        index=True,
    )

    # invoice_id = fields.Char(
    #     string=_("Provider Invoice"),
    #     index=True,
    # )
    #
    dealer_id = fields.Many2one(
        comodel_name="res.partner",
        required=True,
        string=_("Dealer"),
        domain=[
            ('active', '=', True),
            ('is_company', '=', True)
        ],
        index=True,
        tracking=True
    )
    #
    # subscription_id = fields.One2many(
    #     comodel_name='sale.subscription',
    #     inverse_name='gpsdevice_id',
    #     string=_("Subscription"),
    #     readonly=True
    # )
    #
    serial_number_id = fields.Many2one(
        comodel_name="stock.production.lot",
        required=True,
        string=_("Serial Number"),
        index=True,
    )
    active = fields.Boolean(
        default=True
    )

    purchase_date = fields.Date(
        default=fields.Date.today,
        string=_("Purchase Date"),
    )

    device_pin = fields.Char(
        string=_("Device PIN"),
    )

    vehicle_id = fields.Many2one(
        comodel_name="lmm.vehicle",
        ondelete="set null",
        string=_("Installed On"),
        index=True,
        tracking=True,
    )

    accessory_ids = fields.One2many(
        comodel_name="lmm.accessory",
        inverse_name="device_id",
        string=_("Accessories"),
    )

    accessories_count = fields.Integer(
        string=_("Accessories Count"),
        compute='_compute_accessories_count',
    )

    def _compute_accessories_count(self):
        for rec in self:
            rec.accessories_count = self.env['lmm.accessory'].search_count(
                [('device_id', '=', rec.id)]
            )

    @api.model
    @api.depends('warranty_term', 'warranty_start_date')
    def _compute_end_warranty(self):
        if not (self.warranty_term and self.warranty_start_date):
            self.warranty_end_date = None
        else:
            months = int(self.warranty_term[:2])
            start = fields.Date.from_string(self.warranty_start_date)
            self.warranty_end_date = start + timedelta(months * 365 / 12)

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name

        return super(Device, self).copy(default)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The device id must be unique"),
    ]