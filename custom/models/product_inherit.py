from odoo import api, fields, models, _

class ProductInherit(models.Model):
    _inherit = 'product.template'

    no_of_unit_in_carton=fields.Char('Number of units in a carton')
    no_of_cartons_per_layer=fields.Char('Number of cartons per layer')
    no_of_layers_full_pallet=fields.Char('Number of layers full pallet')
    net_weight=fields.Char('Net weight')
    gross_weight=fields.Char('Gross weight')
    ean13=fields.Char('Single unit barcode ')
    ean14=fields.Char('Carton barcode')