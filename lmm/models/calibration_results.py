from odoo import fields, models, api, _


class CalibrationResults(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'lmm.calibration_results'
    _description = 'Calibration Results'

    name = fields.Char(
        required=True,
        string=_("Internal Id"),
        default="Autogenerated on Save",
    )

    calibration_id = fields.Many2one(
        comodel_name="lmm.calibration",
        required=False,
        string=_("Calibration"),
    )

    size = fields.Float(
        digits=(16, 2),
        string=_('Size')
    )

    volts = fields.Float(
        digits=(16, 2),
        string=_('Volts')
    )

    adc = fields.Float(
        digits=(16, 2),
        string=_('Adc')
    )

    volume = fields.Float(
        digits=(16, 2),
        string=_('Volume')
    )

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('lmm.calibration_results') or _('New')
        vals['name'] = seq
        return super(CalibrationResults, self).create(vals)

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(CalibrationResults, self).copy(default)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The calibration results id must be unique"),
    ]
