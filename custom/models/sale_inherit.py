from odoo import api, fields, models, _


class Sale_Inherite(models.Model):
    _inherit = 'sale.order'

    carrier_id = fields.Many2one('delivery.carrier', 'Carrier', required=True, ondelete='cascade')
    effective_date = fields.Date('Effective Date', required=True)
    custom_id = fields.Char("Custom ID")


class Sale_Inherit_line(models.Model):
    _inherit = 'sale.order.line'
    new_route = fields.Many2one('stock.location.route', 'Route')
    bruto_weight = fields.Float('Bruto Weight')
    nett_weight = fields.Float('Nett Weight')


class Vender_bills_new(models.Model):
    _inherit = 'account.move'

    # vender bill fields
    new_account = fields.Many2one('account.account', 'Account')
    new_account_date = fields.Date('Account Date')
    new_ref_des = fields.Char('Reference/Description')

    # invoice fields
    new_incoterms_id = fields.Many2one('account.incoterms', 'Incoterms')
    currency_id = fields.Many2one('res.currency', string='Currency')
    custom_id = fields.Char("Custom ID")

    # new_tax_line_id = fields.One2many('new.tax.line','parent_id','tax line')


# class new_tax_line(models.Model):
#     _name = 'new.tax.line'
#
#     parent_id = fields.Many2one('account.move', 'parent id')
#     tax_desc = fields.Char('Tax Description')
#     tax_acc = fields.Many2one('account.account','Tax Account')
#     total_amount = fields.Monetory('Amount Total')

class Product_new(models.Model):
    _inherit = 'product.template'

    box_ean14 = fields.Char('Box EAN14')
    bruto_weight = fields.Float('Bruto Weight')
    product_tray = fields.Integer('Consumable Products/Tray')
    per_layes = fields.Integer('Trays per layer')
    per_europallet = fields.Integer('Layers per europallet')

    hs_code = fields.Char(
        string="HS Code",
        help="Standardized code for international shipping and goods declaration. At the moment, only used for the FedEx shipping provider.",
    )
    landed_cost_ok = fields.Boolean('Is a Landed Cost', help='Indicates whether the product is a landed cost.')
    can_be_expensed = fields.Boolean(string="Can be Expensed", compute='_compute_can_be_expensed',
                                     store=True, readonly=False,
                                     help="Specify whether the product can be selected in an expense.")
    custom_id = fields.Char("Custom ID")
    new_tax_line_id = fields.One2many('product.customerinfo', 'prod_cust_id', 'tax line')


class product_customerinfo_line(models.Model):
    _name = 'product.customerinfo'

    prod_cust_id = fields.Many2one('product.template', 'Product Custom ID')
    name = fields.Many2one('res.partner', 'Customer')
    product_id = fields.Many2one('product.product', 'Product Variant')
    product_name = fields.Char('Customer Product Name')
    product_code = fields.Char('Customer Product Code')
    min_qty = fields.Float('Minimal Quantity')
    price = fields.Float('Price')
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')


class Contact_Inherit(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean('Is a customer')
    is_vendor = fields.Boolean('Is a Vendor')
    created_by_custom = fields.Many2one(comodel_name="res.users", string="Created by")
    custom_id = fields.Char("Custom ID")


class Purchase_Inherit(models.Model):
    _inherit = 'purchase.order'

    company_id = fields.Many2one('res.company', required=True)
    custom_id = fields.Char("Custom ID")
