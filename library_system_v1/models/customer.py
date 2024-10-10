from odoo import models, fields, api
from odoo.fields import Datetime, Date


# noinspection PyTypeChecker
class Customer(models.Model):
    _name = 'customer'
    _description = 'Customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'name'

    name = fields.Char(default='Customer')
    phone = fields.Char()
    due = fields.Float(readonly=1)
    code = fields.Char(compute="_compute_code_name", default='new', tracking=1)

    def _compute_code_name(self):
        for rec in self:
            rec.code = 'C' + str(rec.id).zfill(5)

