from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date
import re


class Sale_Inherite(models.Model):
    _inherit = 'sale.order'

    carrier_id = fields.Many2one('delivery.carrier', string='Carrier', ondelete='cascade')
    effective_date = fields.Date('Effective Date', required=True)
    custom_id = fields.Char("Custom ID")


class Sale_Inherit_line(models.Model):
    _inherit = 'sale.order.line'

    new_route = fields.Many2one('stock.route', 'Route')
    bruto_weight = fields.Float('Brut Weight', compute="set_weight")
    nett_weight = fields.Float('Nett Weight', compute="set_weight")

    @api.depends('product_uom_qty')
    def set_weight(self):
        for rec in self:
            rec.bruto_weight = float(rec.product_id.bruto_weight) * rec.product_uom_qty
            rec.nett_weight = float(rec.product_id.net_weight) * rec.product_uom_qty

    def _update_taxes(self):
        if not self.product_id:
            return
        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        self._compute_tax_id()
        prd_price = 0.0
        # Commented the below code so that on change of product or Qty Unit Price should not get affected
        prd_price = self.product_id.new_tax_line_id.filtered(lambda
                                                                 rec: rec.name.id == self.order_id.partner_id.id and rec.prod_cust_id.default_code == self.product_id.default_code and self.product_uom_qty >= rec.min_qty and rec.company_id == self.company_id).mapped(
            'price')
        # for i in self.product_id.new_tax_line_id:
        #     if (i.date_start and i.date_end is False):
        #         prd_price = self.product_id.new_tax_line_id.filtered(lambda rec: rec.name.id == self.order_id.partner_id.id and rec.prod_cust_id.default_code == self.product_id.default_code and self.product_uom_qty >= rec.min_qty and rec.company_id == self.company_id).mapped(
        #             'price')
        # elif (i.date_start is False and i.date_end is not False):
        #     prd_price = self.product_id.new_tax_line_id.filtered(lambda rec: rec.name.id == self.order_id.partner_id.id and rec.prod_cust_id.default_code == self.product_id.default_code and self.product_uom_qty >= rec.min_qty and rec.company_id == self.company_id and date.today() <= rec.date_end).mapped(
        #         'price')
        # elif (i.date_start is not False and i.date_end is False):
        #     prd_price = self.product_id.new_tax_line_id.filtered(lambda rec: rec.name.id == self.order_id.partner_id.id and rec.prod_cust_id.default_code == self.product_id.default_code and self.product_uom_qty >= rec.min_qty and rec.company_id == self.company_id and rec.date_start <= date.today()).mapped(
        #         'price')
        # else:
        #     prd_price = self.product_id.new_tax_line_id.filtered(lambda rec: rec.name.id == self.order_id.partner_id.id and rec.prod_cust_id.default_code == self.product_id.default_code and self.product_uom_qty >= rec.min_qty and rec.company_id == self.company_id and rec.date_start <= date.today() <= rec.date_end).mapped('price')
        if prd_price:
            vals['price_unit'] = prd_price[0]
        # if self.order_id.pricelist_id and self.order_id.partner_id:
        else:
            vals['price_unit'] = product._get_tax_included_unit_price(
                self.company_id,
                self.order_id.currency_id,
                self.order_id.date_order,
                'sale',
                fiscal_position=self.order_id.fiscal_position_id,
                product_price_unit=self._get_display_price(product),
                product_currency=self.order_id.currency_id
            )
        self.update(vals)

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            # Commented the below code so that on change of product or Qty Unit Price should not get affected
            prd_price = 0.0
            prd_price = self.product_id.new_tax_line_id.filtered(lambda
                                                                     rec: rec.name.id == self.order_id.partner_id.id and rec.prod_cust_id.default_code == self.product_id.default_code and self.product_uom_qty >= rec.min_qty and rec.company_id == self.company_id).mapped(
                'price')
            # for i in self.product_id.new_tax_line_id:
            #     if (i.date_start and i.date_end is False):
            #         prd_price = self.product_id.new_tax_line_id.filtered(lambda
            #                                                                  rec: rec.name.id == self.order_id.partner_id.id and rec.prod_cust_id.default_code == self.product_id.default_code and self.product_uom_qty >= rec.min_qty and rec.company_id == self.company_id).mapped(
            #             'price')
            #     # elif (i.date_start is False and i.date_end is not False):
            #     #     prd_price = self.product_id.new_tax_line_id.filtered(lambda
            #     #                                                              rec: rec.name.id == self.order_id.partner_id.id and rec.prod_cust_id.default_code == self.product_id.default_code and self.product_uom_qty >= rec.min_qty and rec.company_id == self.company_id and date.today() <= rec.date_end).mapped(
            #     #         'price')
            #     # elif (i.date_start is not False and i.date_end is False):
            #     #     prd_price = self.product_id.new_tax_line_id.filtered(lambda
            #     #                                                              rec: rec.name.id == self.order_id.partner_id.id and rec.prod_cust_id.default_code == self.product_id.default_code and self.product_uom_qty >= rec.min_qty and rec.company_id == self.company_id and rec.date_start <= date.today()).mapped(
            #     #         'price')
            #     else:
            #         prd_price = self.product_id.new_tax_line_id.filtered(lambda
            #                                                                  rec: rec.name.id == self.order_id.partner_id.id and rec.prod_cust_id.default_code == self.product_id.default_code and self.product_uom_qty >= rec.min_qty and rec.company_id == self.company_id and rec.date_start <= date.today() <= rec.date_end).mapped(
            #             'price')
            if prd_price:
                self.price_unit = prd_price[0]
            else:
                self.price_unit = product._get_tax_included_unit_price(
                    self.company_id or self.order_id.company_id,
                    self.order_id.currency_id,
                    self.order_id.date_order,
                    'sale',
                    fiscal_position=self.order_id.fiscal_position_id,
                    # product_price_unit=self._get_display_price(product),
                    product_price_unit=self._get_display_price(),
                    product_currency=self.order_id.currency_id
                )

    def _get_protected_fields(self):
        return [
            'product_id', 'name', 'product_uom', 'tax_id', 'analytic_tag_ids'
        ]

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
    partner_id = fields.Many2one('res.partner', 'Customer')
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
    vies_failed_message = fields.Char("")


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
