# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)


class Characterization(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'lmm.characterization'
    _description = "Characterization"
    
    name = fields.Char(
        required=True,
        string=_("Internal Id"),
    )

    fuel_sensor_id = fields.Many2one(
        comodel_name="lmm.fuel_sensor",
        required=True,
        string=_("Sensor"),
    )

    serial_number = fields.Many2one(
        related='fuel_sensor_id.serial_number_id',
        store=True,
        depends=['fuel_sensor_id']
    )

    fuel_characterization_detail_ids = fields.One2many(
        comodel_name="lmm.characterization_detail",
        inverse_name="fuel_characterization_id",
        string=_("Characterization"),
    )

    volt_min = fields.Float(
        digits=(16, 3),
        string=_('Volt min')
    )

    volt_max = fields.Float(
        digits=(16, 3),
        string=_('Volt max')
    )

    process_type = fields.Selection(
        selection=[
            ("automatic", _("Automatic")),
            ("manual", _("Manual")),
        ],
        default="manual",
        string=_("Process Type"),
        tracking=True
    )

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Characterization, self).copy(default)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The characterization id must be unique"),
    ]