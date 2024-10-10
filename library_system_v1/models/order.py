from odoo import models, fields, api
from odoo.fields import Datetime, Date
from odoo.exceptions import UserError, ValidationError


# noinspection PyTypeChecker
class Order(models.Model):
    _name = 'order'
    _description = 'Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'ref'

    ref = fields.Char(compute="_compute_order_name", default='new', tracking=1)
    customer_id = fields.Many2one('customer')
    customer_phone = fields.Char(related='customer_id.phone')
    customer_code = fields.Char(related='customer_id.code')
    date = fields.Date(readonly=1, default=fields.Datetime.now())
    order_line_ids = fields.One2many('order.line', 'order_id')
    total = fields.Char(string="Total", tracking=1, compute="_compute_total_price")

    state = fields.Selection([
        ('new', 'New'),
        ('completed', 'Completed')],
        default='new', tracking=1
    )

    def action_completed(self):
        for rec in self:
            for line in rec.order_line_ids:
                if line.book_id.number > 0 and line.book_id.number >= line.quantity:
                    line.book_id.number -= line.quantity
                else:
                    raise ValidationError('Sorry Required Quantity > In Hand Quantity !')
            rec.state = 'completed'

    def _compute_order_name(self):
        for rec in self:
            rec.ref = 'OR' + str(rec.id).zfill(5)

    @api.depends('order_line_ids', 'order_line_ids.quantity', 'order_line_ids.book_id')
    def _compute_total_price(self):
        for rec in self:
            total_value = 0
            for line in rec.order_line_ids:
                total_value += line.total_price
            rec.total = total_value


# noinspection PyTypeChecker
class OrderLine(models.Model):
    _name = 'order.line'
    _description = 'Order Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'book_id'

    order_id = fields.Many2one('order')
    book_id = fields.Many2one(
        'book', tracking=1
    )
    quantity = fields.Integer()
    number_in_hand = fields.Integer(related='book_id.number')
    unit_price = fields.Float(related='book_id.price')
    total_price = fields.Float(compute='_compute_total_price')

    @api.depends('quantity', 'book_id')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = rec.unit_price * rec.quantity
