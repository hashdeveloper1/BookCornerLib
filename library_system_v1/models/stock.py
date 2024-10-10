from odoo import models, fields, api
from odoo.fields import Datetime, Date


# noinspection PyTypeChecker
class Stock(models.Model):
    _name = 'stock'
    _description = 'Stock'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'code'

    code = fields.Char(compute="_compute_code_name", default='new', tracking=1)
    book_id = fields.Many2one(
        'book', tracking=1
    )
    number = fields.Integer()

    state = fields.Selection([
        ('new', 'New'),
        ('completed', 'Completed')],
        default='new', tracking=1
    )

    def _compute_code_name(self):
        for rec in self:
            rec.code = 'OP' + str(rec.id).zfill(5)

    def action_completed(self):
        for rec in self:
            rec.state = 'completed'
            rec.book_id.number += rec.number
