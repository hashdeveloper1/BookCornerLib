from odoo import models, fields, api
from odoo.fields import Datetime, Date


# noinspection PyTypeChecker
class Book(models.Model):
    _name = 'book'
    _description = 'Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'name'

    name = fields.Char(default='Book')
    cost = fields.Float()
    price = fields.Float()
    number = fields.Integer(readonly=1, tracking=1)
    code = fields.Char(compute="_compute_code_name", default='new', tracking=1)
    peper_type = fields.Selection([
        ('1', 'ورق أبيض'),
        ('2', 'ورق شمواه')],
        tracking=1,
    )

    def _compute_code_name(self):
        for rec in self:
            rec.code = 'B' + str(rec.id).zfill(5)
