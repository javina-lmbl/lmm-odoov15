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

    fleetrun = fields.Boolean(
        default=False,
        string=_("Fleetrun"),
        tracking=True
    )

    speaker = fields.Boolean(
        default=False,
        string=_("Speaker"),
    )

    anti_jammer_blocker = fields.Boolean(
        default=False,
        string=_("Anti Jammer Blocker"),
    )

    smart_blocker = fields.Boolean(
        default=False,
        string=_("Smart Blocker"),
    )

    blocker = fields.Boolean(
        default=False,
        string=_("Blocker"),
    )

    scanner = fields.Boolean(
        default=False,
        string="Scanner",
        tracking=True
    )

    padlock = fields.Boolean(
        default=False,
        string=_("Padlock"),
    )

    solar_panel = fields.Boolean(
        default=False,
        string=_("Solar Panel"),
    )

    temperature = fields.Boolean(
        default=False,
        string=_("Temperature"),
        tracking=True
    )

    ibutton = fields.Boolean(
        default=False,
        string=_("iButton"),
    )

    microphone = fields.Boolean(
        default=False,
        string=_("Microphone"),
    )

    sheet = fields.Boolean(
        default=False,
        string=_("Sheet"),
    )

    opening_sensor = fields.Boolean(
        default=False,
        string=_("Opening Sensor"),
    )

    logistic = fields.Boolean(
        default=False,
        string=_("Logistic"),
        tracking=True
    )

    collective = fields.Boolean(
        default=False,
        string=_("Collective"),
        tracking=True
    )

    fuel_hall = fields.Boolean(
        default=False,
        string=_("Efecto Hall"),
        tracking=True
    )

    disengagement_sensor = fields.Boolean(
        default=False,
        string=_("Disengagement Sensor"),
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

    datetime_gps = fields.Datetime(
        string=_("DateTime GPS"),
    )

    datetime_server = fields.Datetime(
        string=_("DateTime Server"),
    )

    last_position = fields.Char(
        string=_("Last Position"),
    )

    last_report = fields.Integer(
        string=_("Last Report"),
        compute="_compute_last_report",
        store=True,
        help="Time without reporting in platforms expressed in hours",
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
        domain=[
            ('default_code', '=like', 'CGPS%')
        ],
        required=True,
        string=_("Product Type"),
        index=True,

    )

    invoice_id = fields.Char(
        string=_("Provider Invoice"),
        index=True,
    )

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

    electronics = fields.Boolean(
        default=False,
        string=_("Electronics"),
        tracking=True,
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

    @api.onchange('product_id')
    def onchange_get_serialnumbers_for_selected_product(self):
        _logger.warning('Product ID: %s', self.product_id.name)
        _logger.warning('Product Name: %s', self.product_id)
        domain = {}
        if self.product_id:
            domain = {'domain': {'serial_number_id': [('product_id', '=', self.product_id.id)]}}
            _logger.warning('Domain Output: %s', domain)
        return domain

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