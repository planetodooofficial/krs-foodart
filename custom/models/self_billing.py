import math
from datetime import datetime, date

from datetime import timedelta
from odoo import fields, models, api, _, tools


class SelfBilling(models.Model):
    _name = 'self.billing'

    name = fields.Char(string='Name')
    address = fields.Many2one('res.partner', string="Address")
    order_date = fields.Date('Start date')
    end_date = fields.Date('End date')
    invoice_created = fields.Boolean('Invoice created')
    billing_o2m = fields.One2many("self.billing.line", 'billing_m2o')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('rejected', 'Rejected'),
        ('edited', 'Edited'),
    ], default='draft', string='Status')


class SelfBillingLine(models.Model):
    _name = 'self.billing.line'

    # product = fields.Many2one('product.product', 'Description')
    product = fields.Char('Description')
    quantity = fields.Char('Quantity')
    uom = fields.Char('Uom')
    reduction = fields.Char('Pricelist/reduction')
    unit_price = fields.Float('Unit price (Excl. VAT)')
    discount = fields.Integer('Discount')
    net_price = fields.Float('Net price (Excl. VAT)')
    vat = fields.Char(string='VAT(%)')
    vat_amount = fields.Integer('VAT(€)')
    total = fields.Float('Total (Excl. VAT)')
    billing_m2o = fields.Many2one('self.billing')
