from odoo import api, fields, models, _


class ProductInherit(models.Model):
    _inherit = 'product.template'

    no_of_unit_in_carton = fields.Char('Number Of Units In a Carton')
    no_of_cartons_per_layer = fields.Char('Number Of Cartons Per Layer')
    no_of_layers_full_pallet = fields.Char('Number Of Layers Full Pallet')
    net_weight = fields.Char('Net Weight')
    gross_weight = fields.Char('Gross Weight')
    ean13 = fields.Char('Single Unit Barcode/ EAN13')
    ean14 = fields.Char('Carton Barcode/ EAN14')

    # Dates Group
    new_use_time = fields.Integer('Product Use Time')
    new_life_time = fields.Integer('Product Life Time')
    new_removeal_time = fields.Integer('Product Removal Time')
    new_alert_time = fields.Integer('Product Alert Time')
