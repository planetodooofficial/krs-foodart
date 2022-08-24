from odoo import fields, api, models, _


class InheritStockInventoryAdjust(models.TransientModel):
    _inherit = 'stock.inventory.adjustment.name'

    forced_date = fields.Datetime(string="Forced Date")

    def action_apply(self):
        res = super(InheritStockInventoryAdjust, self).action_apply()
        for id in self.quant_ids.ids:
            self._cr.execute(f"""UPDATE stock_quant SET create_date='{self.forced_date}' WHERE id='{id}'""")

    # mehul's code start from here

        for id in self.quant_ids.ids:
            self._cr.execute(f"""UPDATE stock_quant SET create_date='{self.forced_date}' WHERE id={id}""")
            # print("self.quant_ids.product_name", self.quant_ids.product_name)
            # print("self.quant_ids.default_code", self.quant_ids.default_code)
            search_product = self.env['product.product'].search([('name', '=', self.quant_ids.product_name),
                                                                 ('default_code', '=', self.quant_ids.default_code)])
            # print(search_product)
            search_product_stock_valuation = self.env["stock.valuation.layer"].search(
                [('product_id', '=', search_product.id)])
            search_product_stock_quant = self.env["stock.quant"].search([('product_id', '=', search_product.id)])
            print(search_product_stock_quant)
            # stock_valuation = self.env["stock.valuation.layer"]
            # print(stock_valuation)
            search_product._cr.execute(
                f"""UPDATE product_product SET write_date='{self.forced_date}' WHERE id={search_product.id}""")

            search_product_stock_quant._cr.execute(
                f"""UPDATE stock_quant SET create_date='{self.forced_date}' WHERE id={search_product_stock_quant.ids[-1]}""")
            search_product_stock_valuation._cr.execute(
                f"""UPDATE stock_valuation_layer SET create_date='{self.forced_date}' WHERE id={search_product_stock_valuation.ids[-1]}""")

            stock_move_line = self.env["stock.move.line"].search([('product_id', '=', search_product.id)])
            print(list(stock_move_line.ids))
            stock_move_line._cr.execute(
                f"""UPDATE stock_move_line SET date='{self.forced_date}' WHERE id={list(stock_move_line.ids)[-1]}""")
            stock_move_line._cr.execute(
                f"""UPDATE stock_move_line SET write_date='{self.forced_date}' WHERE id={list(stock_move_line.ids)[-1]}""")
            stock_move_line._cr.execute(
                f"""UPDATE stock_move_line SET create_date='{self.forced_date}' WHERE id={list(stock_move_line.ids)[-1]}""")
