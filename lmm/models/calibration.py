from odoo import fields, models, api,_


class FuelCalibration(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'lmm.calibration'
    _description = 'Calibration'

    name = fields.Char(
        required=True,
        string=_("Calibration"),
        default="Autogenerated on Save",
        copy=False
    )

    fuel_sensor_id = fields.Many2one(
        comodel_name="lmm.fuel_sensor",
        string=_("Fuel Sensor Installed"),
        index=True,
        tracking=True
    )

    method = fields.Selection([
        ('characterization', _('Characterization')),
        ('pattern_jug', _('Pattern jug')),
        ('calibrator', _('Calibration'))
    ],
        default="characterization",
        string=_("Method")
    )

    correction = fields.Float(
        digits=(16, 2),
        string=_('Correction')
    )

    img1 = fields.Image(string=_('Img 1'))
    img2 = fields.Image(string=_('Img 2'))
    img3 = fields.Image(string=_('Img 3'))

    calibration_results_ids = fields.One2many(
        comodel_name="lmm.calibration_results",
        inverse_name="calibration_id",
        string=_("Calibration Results"),
    )

    calibration_results_count = fields.Integer(
        string=_("Calibration Results Count"),
        compute='_compute_calibration_results_count',
    )

    def _compute_calibration_results_count(self):
        for rec in self:
            rec.calibration_results_count = self.env['lmm.calibration_results'].search_count(
                [('calibration_id', '=', rec.id)]
            )

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('lmm.calibration') or _('New')
        vals['name'] = seq
        return super(FuelCalibration, self).create(vals)

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(FuelCalibration, self).copy(default)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The calibration id must be unique"),
    ]
