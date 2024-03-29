from odoo import fields, models, api,_


class FuelLoadDivision(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'lmm.fuel_load_division'
    _description = 'Fuel load division'

    name = fields.Char(
        required=True,
        string=_("Internal Id"),
        default="Autogenerated on Save",
        copy=False
    )

    min_volume = fields.Float(
        digits=(16, 9),
        string=_('Min Volume')
    )

    max_volume = fields.Float(
        digits=(16, 9),
        string=_('Max volume')
    )

    fuel_step_load_count = fields.Integer(
        string=_("Fuel Tanks Count"),
        compute='_compute_fuel_step_count',
    )

    def _compute_fuel_step_count(self):
        for rec in self:
            rec.fuel_step_load_count = self.env['lmm.fuel_step_load'].search_count(
                [('fuel_load_division_id', '=', rec.id)]
            )

    def action_view_fuel_steps(self):
        action = self.env['ir.actions.act_window']._for_xml_id('lmm.lmm_fuel_step_load_list_action')
        action['context'] = {'active_test': False}
        action['context'] = {'fuel_load_division_id': self.id}
        action['domain'] = [('fuel_load_division_id.id', '=', self.id)]
        return action

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('lmm.fuel_load_division') or _('New')
        vals['name'] = seq
        return super(FuelLoadDivision, self).create(vals)

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(FuelLoadDivision, self).copy(default)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The fuel load division id must be unique"),
    ]