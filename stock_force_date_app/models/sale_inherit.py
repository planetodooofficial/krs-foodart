from odoo import api, fields, models, _


class SaleInherit(models.Model):
    _inherit = "sale.order"

    def _prepare_confirmation_values(self):
        rec = {'state': 'sale'}
        if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
            return rec
        return {**rec, **{'date_order': fields.Datetime.now()}}
