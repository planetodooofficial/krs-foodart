from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re

class Sale_Inherite(models.Model):
    _inherit = 'sale.order'

    carrier_id = fields.Many2one('delivery.carrier', 'Carrier', ondelete='cascade')
    effective_date = fields.Date('Effective Date', required=True)
    custom_id = fields.Char("Custom ID")


class Sale_Inherit_line(models.Model):
    _inherit = 'sale.order.line'

    new_route = fields.Many2one('stock.location.route', 'Route')
    bruto_weight = fields.Float('Brut Weight', compute="set_weight")
    nett_weight = fields.Float('Nett Weight', compute="set_weight")

    @api.depends('product_uom_qty')
    def set_weight(self):
        for rec in self:
            rec.bruto_weight = float(rec.product_id.bruto_weight) * rec.product_uom_qty
            rec.nett_weight = float(rec.product_id.net_weight) * rec.product_uom_qty


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
    company_id = fields.Many2one('res.company', 'Company')


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


class Project_inherit_new(models.Model):
    _inherit = 'project.project'

    allow_forecast = fields.Boolean('Allow forecast')
    sub_task_project_new = fields.Many2one('project.project', 'Sub-task Project')


class Inherit_Manufacture(models.Model):
    _inherit = 'mrp.production'

    new_availability = fields.Selection(
        [('assigned', 'Available'), ('partially_available', 'Partially Available'), ('waiting', 'Waiting'),
         ('none', 'None')],
        'Materials Availability')
