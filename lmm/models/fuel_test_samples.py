from odoo import fields, models, api, _


class FuelTestSamples(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'lmm.fuel_test_samples'
    _description = 'Description'

    name = fields.Char(
        required=True,
        string=_("Fuel Test Sample"),
        default="Autogenerated on Save",
    )

    sample_number = fields.Integer(
        string=_("Sample No")
    )

    fuel_tank_id = fields.Many2one(
        comodel_name="lmm.fuel_tank",
        string=_("Fuel Tank"),
        index=True,
        tracking=True
    )

    volume = fields.Float(
        digits=(16, 2),
        string=_('Volume')
    )

    diff = fields.Float(
        digits=(16, 2),
        string=_('Diff')
    )

    fuel_test_id = fields.Many2one(
        comodel_name="lmm.fuel_test",
        string=_("Fuel Test"),
        index=True,
        tracking=True
    )

    fuel_sensor_id = fields.Many2one(
        comodel_name="lmm.fuel_sensor",
        string=_("Fuel Sensor"),
        index=True,
        tracking=True
    )

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('lmm.fuel_test_samples') or _('New')
        vals['name'] = seq
        return super(FuelTestSamples, self).create(vals)

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(FuelTestSamples, self).copy(default)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The fuel test sample id must be unique"),
    ]
