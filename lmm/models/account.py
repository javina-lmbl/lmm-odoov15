from odoo import fields, models, api, _


class Account(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'lmm.account'
    _description = 'Description'

    name = fields.Char(
        required=True,
        string=_("Account")
    )

    type = fields.Selection([
        ('dealer', _('dealer')),
        ('wholesaler', _('Wholesaler')),
        ('retail', _('Retail')),
        ('client', _('Client'))
    ],
        default="dealer",
        string=_("Type"),
        tracking=True
    )

    client_id = fields.Many2one(
        comodel_name="res.partner",
        required=True,
        string=_("Parent Account"),
        domain=[
            ('active', '=', True),
            ('is_company', '=', True)
        ],
        index=True,
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
        return super(Account, self).copy(default)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The account name must be unique"),
    ]