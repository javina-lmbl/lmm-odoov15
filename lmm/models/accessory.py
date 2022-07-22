# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, models, fields, _
from odoo.exceptions import Warning


class Accessory(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'lmm.accessory'
    _description = 'Accessories module'

    name = fields.Char(
        required=True,
        string=_("Internal Id"),
        default="Autogenerated on Save",
        copy=False
    )

    serial_number_id = fields.Many2one(
        comodel_name="stock.production.lot",
        string=_("Serial Number"),
        index=True,
        tracking=True
    )

    client_id = fields.Many2one(
        comodel_name="res.partner",
        string=_("Client"),
        domain=[
            ('active', '=', True),
            ('is_company', '=', True)
        ],
        index=True,
        tracking=True
    )

    device_id = fields.Many2one(
        comodel_name="lmm.device",
        ondelete="set null",
        string=_("Assigned To"),
        index=True,
        tracking=True,
    )

    installation_date = fields.Date(
        default=fields.Date.today,
        string=_("Installation Date"),
        tracking=True
    )

    status = fields.Selection(
        selection=[
            ("drop", _("Drop")),
            ("comodato", _("Comodato")),
            ("courtesy", _("Courtesy")),
            ("demo", _("Demo")),
            ("uninstalled", _("Uninstalled")),
            ("external", _("External")),
            ("hibernate", _("Hibernate")),
            ("installed", _("Installed")),
            ("inventory", _("Inventory")),
            ("new", _("New")),
            ("ready", _("Ready to Install")),
            ("borrowed", _("Borrowed")),
            ("tests", _("Tests")),
            ("replacement", _("Replacement")),
            ("backup", _("Backup")),
            ("rma", _("RMA")),
            ("sold", _("Sold")),
        ],
        default="inventory",
        string=_("Status"),
        tracking=True,
    )

    product_id = fields.Many2one(
        comodel_name="product.product",
        required=True,
        string=_("Product Type"),
        index=True
    )

    provider_invoice = fields.Char(
        string=_("Provider Invoice"),
        index=True,
    )

    purchase_date = fields.Date(
        default=fields.Date.today,
        string=_("Purchase Date"),
        tracking=True
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
        ],
        default="12",
        string=_("Warranty Term"),
    )

    assigned_tickets = fields.Integer(
        string=_("Tickets Count"),
        compute='_compute_assigned_tickets_count',
    )

    vehicle_id = fields.Many2one(
        comodel_name="lmm.vehicle",
        ondelete="set null",
        string=_("Installed On"),
        index=True,
        tracking=True,
    )

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('lmm.accessory') or _('New')
        vals['name'] = seq
        return super(Accessory, self).create(vals)

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Accessory, self).copy(default)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The accessory id must be unique"),
    ]

    def btn_remove_from_gpsdevice(self):
        for accessory in self:
            if not accessory.gpsdevice_id:
                raise Warning('El accesorio %s no esta asignado a un dispositivo gps' % accessory.name)
            else:
                today = fields.Date.today()
                gpsdevice = accessory.gpsdevice_id

                gpsdevice.message_post(
                    body="Accesorio <b>" + accessory.name + "</b> desinstalado el día <b>" + today.strftime(
                        '%d-%m-%Y') + "</b> <br>No Serie: <b>" + accessory.serialnumber_id.name + "</b>")

                accessory.message_post(
                    body="Accesorio desinstalado del equipo <b>" + gpsdevice.name + "</b> el día <b>" + today.strftime(
                        '%d-%m-%Y') +'</b>')

                accessory.write({'gpsdevice_id': None, 'status': 'uninstalled'})
        return True

    def _compute_assigned_tickets_count(self):
        for rec in self:
            rec.assigned_tickets = self.env['helpdesk.ticket'].search_count(
                [('accessory_id', '=', rec.id)])

    @api.model
    @api.depends('warranty_term', 'warranty_start_date')
    def _compute_end_warranty(self):
        if not (self.warranty_term and self.warranty_start_date):
            self.warranty_end_date = None
        else:
            months = int(self.warranty_term[:2])
            start = fields.Date.from_string(self.warranty_start_date)
            self.warranty_end_date = start + timedelta(months * 365 / 12)
