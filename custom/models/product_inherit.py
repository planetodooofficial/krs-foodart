from odoo import api, fields, models, _
import re
from odoo.exceptions import ValidationError


class ProductInherit(models.Model):
    _inherit = 'product.template'

    net_weight = fields.Char('Net Weight')
    gross_weight = fields.Char('Gross Weight')
    ean13 = fields.Char('Single Unit Barcode/ EAN13')
    ean14 = fields.Char('Carton Barcode/ EAN14')

    # Dates Group
    new_use_time = fields.Integer('Product Use Time')
    new_life_time = fields.Integer('Product Life Time')
    new_removeal_time = fields.Integer('Product Removal Time')
    new_alert_time = fields.Integer('Product Alert Time')

    box_ean14 = fields.Char('Box EAN14')
    bruto_weight = fields.Float('Bruto Weight')
    product_tray = fields.Integer('Consumable Products/Tray')
    per_layes = fields.Integer('Trays per layer')
    per_europallet = fields.Integer('Layers per europallet')

    @api.onchange('net_weight')
    def check_net_weight(self):
        try:
            float(self.net_weight)
        except:
            raise ValidationError('Value Should be Integer for Float Only !')

    hs_code = fields.Char(
        string="HS Code",
        help="Standardized code for international shipping and goods declaration. At the moment, only used for the FedEx shipping provider.",
    )
    landed_cost_ok = fields.Boolean('Is a Landed Cost', help='Indicates whether the product is a landed cost.')
    can_be_expensed = fields.Boolean(string="Can be Expensed", compute='_compute_can_be_expensed',
                                     store=True, readonly=False,
                                     help="Specify whether the product can be selected in an expense.")
    custom_id = fields.Char("Custom ID")
    new_tax_line_id = fields.One2many('product.customerinfo', 'prod_cust_id', 'Customers')

    @api.depends('type')
    def _compute_can_be_expensed(self):
        self.filtered(lambda p: p.type not in ['consu', 'service']).update({'can_be_expensed': False})


class ProductInherit(models.Model):
    _inherit = 'product.product'

    @api.onchange('net_weight')
    def check_net_weight(self):
        net_weight = re.findall(r'[a-zA-Z]', self.net_weight)
        if self.net_weight and net_weight:
            raise ValidationError("Please Enter Correct Net Weight !")
