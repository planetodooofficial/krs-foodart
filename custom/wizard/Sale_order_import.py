from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class SOWizard(models.TransientModel):
    _name = "so.wizard"
    _description = "SO Wizard"

    load_file = fields.Binary("Load File")

    def import_so_data(self):
        print("Sale order is working")
        csv_data = self.load_file
        file_obj = TemporaryFile('wb+')
        csv_data = base64.decodebytes(csv_data)
        file_obj.write(csv_data)
        file_obj.seek(0)
        str_csv_data = file_obj.read().decode('utf-8')
        lis = csv.reader(io.StringIO(str_csv_data), delimiter=',')
        row_num = 0
        header_list = []
        data_dict = {}
        for row in lis:
            data_dict.update({row_num: row})
            row_num += 1
        for key, value in data_dict.items():
            if key == 0:
                header_list.append(value)
            else:
                print(value)
                order_reference = value[0].strip()
                id = value[1].strip()
                customer = value[2].strip()
                customer_id = value[3].strip()
                invoice_address = value[4].strip()
                delivery_address = value[5].strip()
                quotation_template = value[6].strip()
                validity = value[7] or False
                pricelist = value[8].strip()
                payment_terms = value[9].strip()
                delivery_method = value[10].strip()
                warehouse = value[11].strip()
                incoterm = value[12].strip()
                shipping_policy = value[13].strip()
                expected_date = value[14] or False
                commitment_date = value[15] or False
                effective_date = value[16] or False
                order_date = value[17] or False
                fiscal_position = value[18].strip()
                campaign = value[19].strip()
                medium = value[20].strip()
                source = value[21].strip()
                sales_person = value[22].strip()
                tags = value[23].strip()
                sales_team = value[24].strip()
                customer_reference = value[25].strip()
                online_signature = value[26].strip()
                online_payment = value[27].strip()
                company = value[28].strip()
                source_document = value[29].strip()
                opportunity = value[30].strip()

                warehouse_id = self.env["stock.warehouse"].search([('name', '=', warehouse)], limit=1)
                user_id = self.env["res.users"].search(
                    [('name', '=', sales_person), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                team_id = self.env["crm.team"].search([('name', '=', sales_team)], limit=1)
                company_id = self.env["res.company"].search([('name', '=', company)], limit=1)
                fiscal_position_id = self.env["account.fiscal.position"].search([('name', '=', fiscal_position)],
                                                                                limit=1)
                payment_term_id = self.env["account.payment.term"].search([('name', '=', payment_terms)], limit=1)
                carrier_id = self.env["delivery.carrier"].search([('name', '=', delivery_method)], limit=1)
                tag_ids = self.env["crm.tag"].search([('name', '=', tags)], limit=1)
                # analytic_account_id = self.env["account.analytic.account"].search(
                #     [('name', '=', analytic_account), ('custom_id', '=', analytic_account_id), '|',
                #      ('active', '=', True), ('active', '=', False)], limit=1)
                opportunity_id = self.env["crm.lead"].search([('name', '=', opportunity)], limit=1)

                part_id = self.env["res.partner"].search(
                    [('name', '=', customer), ('id_custom', '=', customer_id), '|', ('active', '=', True),
                     ('active', '=', False)], limit=1)
                invoice_addr = self.env["res.partner"].search(
                    [('parent_id', '=', part_id.id), ("type", "=", 'invoice')], limit=1)
                if not invoice_addr:
                    invoice_addr = part_id

                delivery_addr = self.env["res.partner"].search(
                    [('parent_id', '=', part_id.id), ("type", "=", 'delivery')], limit=1)
                if not delivery_addr:
                    delivery_addr = part_id

                sale_ord_temp_id = self.env["sale.order.template"].search([('name', '=', quotation_template)], limit=1)
                priceli_id = self.env["product.pricelist"].search([('name', '=', pricelist)], limit=1)
                campaign_id = self.env["utm.campaign"].search([('name', '=', campaign)])
                medium_id = self.env["utm.medium"].search([('name', '=', medium)])
                source_id = self.env["utm.source"].search([('name', '=', source)])
                incoterm_id = self.env["account.incoterms"].search([('name', '=', incoterm)])

                search_sale_order = self.env["sale.order"].search(
                    [('name', '=', order_reference), ('custom_so_id', '=', id)])

                so_val = {
                    'custom_id': id,
                    'name': order_reference,
                    'partner_id': part_id.id,
                    'partner_invoice_id': invoice_addr.id,
                    'partner_shipping_id': delivery_addr.id,
                    'sale_order_template_id': sale_ord_temp_id.id,
                    'validity_date': validity,
                    'pricelist_id': priceli_id.id,
                    'payment_term_id': payment_term_id.id,
                    'carrier_id': carrier_id.id,
                    'incoterm': incoterm_id.id,
                    'picking_policy': shipping_policy,
                    'expected_date': expected_date,
                    'commitment_date': commitment_date,
                    'effective_date': effective_date,
                    'date_order': order_date,
                    'fiscal_position_id': fiscal_position_id.id,
                    'campaign_id': campaign_id.id,
                    'medium_id': medium_id.id,
                    'source_id': source_id.id,
                    'user_id': user_id.id,
                    'tag_ids': [(6, 0, tag_ids.ids)],
                    'team_id': team_id.id,
                    'client_order_ref': customer_reference,
                    'require_signature': online_signature,
                    'require_payment': online_payment,
                    'origin': source_document,
                    'opportunity_id': opportunity_id.id,
                }
                if not search_sale_order:
                    so_id = self.env['sale.order'].create(so_val)
                    print("so_id", so_id)
                    print(so_val)

    def create_so_line_data(self):
        print("Sale order line is working")
        csv_data = self.load_file
        file_obj = TemporaryFile('wb+')
        csv_data = base64.decodebytes(csv_data)
        file_obj.write(csv_data)
        file_obj.seek(0)
        str_csv_data = file_obj.read().decode('utf-8')
        lis = csv.reader(io.StringIO(str_csv_data), delimiter=',')
        row_num = 0
        header_list = []
        data_dict = {}
        for row in lis:
            data_dict.update({row_num: row})
            row_num += 1
        for key, value in data_dict.items():
            if key == 0:
                header_list.append(value)
            else:
                print(value)
                sale_order_id = value[0]
                order_lines_is_a_service = value[1]
                order_lines_product = value[2]
                order_lines_internal_reference = value[3]
                order_lines_oem = value[4]
                order_lines_description = value[5]
                order_lines_ordered_quantity = value[6]
                order_lines_delivered_quantity = value[7]
                order_lines_invoiced_quantity = value[8]
                order_lines_unit_of_measure = value[9]
                order_lines_analytic_tags = value[10]
                order_lines_warehouse = value[11]
                order_lines_unit_price = value[12]
                order_lines_taxes = value[13] or None
                order_lines_discount = value[14]
                order_lines_display_type = value[15]

                if not order_lines_product:
                    order_lines_product = 'Service'
                    order_lines_internal_reference = 'Service'
                product_id = False
                product_uom_id = self.env['uom.uom'].search([('name', '=', order_lines_unit_of_measure)], limit=1)
                product_count = self.env['product.product'].search_count(
                    [('name', '=', order_lines_product), '|', ('active', '=', True), ('active', '=', False)])
                if product_count:
                    if product_count > 1:
                        product_id = self.env['product.product'].search(
                            [('uom_id', '=', product_uom_id.id), ('name', '=', order_lines_product),
                             ('default_code', '=', order_lines_internal_reference), '|', ('active', '=', True),
                             ('active', '=', False)], limit=1)
                    else:
                        product_id = self.env['product.product'].search(
                            [('name', '=', order_lines_product), '|', ('active', '=', True), ('active', '=', False)], limit=1)

                analytic_tags_ids = self.env["account.analytic.tag"].search([('name', '=', order_lines_analytic_tags)],
                                                                            limit=1)
                tax_id = self.env["account.tax"].search([('name', '=', order_lines_taxes)], limit=1)
                order_lines_warehouse_id = self.env["stock.warehouse"].search([('name', '=', order_lines_warehouse)],
                                                                              limit=1)
                order_id = self.env["sale.order"].search([('custom_so_id', '=', sale_order_id)])
                lst = []

                if order_id:
                    if order_lines_product and product_id:
                        so_line_vals = {
                            'is_service': True if order_lines_is_a_service == "True" else False,
                            'product_id': product_id.id,
                            'product_oem_code': order_lines_oem,
                            'name': order_lines_description,
                            'product_uom_qty': order_lines_ordered_quantity,
                            'warehouse_id': order_lines_warehouse_id.id,
                            'product_uom': product_uom_id.id,
                            'analytic_tag_ids': [(6, 0, analytic_tags_ids.ids)],
                            'price_unit': order_lines_unit_price,
                            'tax_id': [(6, 0, tax_id.ids)],
                            'discount': order_lines_discount,
                            'display_type': order_lines_display_type if not order_lines_unit_of_measure else None,
                            'order_id': order_id.id
                        }
                        self.env["sale.order.line"].create(so_line_vals)
                    else:
                        lst.append(order_lines_product)
                        order_id.write({'note': lst})

    def change_status_of_so(self):
        print("Change status of so is working")
        csv_data = self.load_file
        file_obj = TemporaryFile('wb+')
        csv_data = base64.decodebytes(csv_data)
        file_obj.write(csv_data)
        file_obj.seek(0)
        str_csv_data = file_obj.read().decode('utf-8')
        lis = csv.reader(io.StringIO(str_csv_data), delimiter=',')
        row_num = 0
        header_list = []
        data_dict = {}
        for row in lis:
            data_dict.update({row_num: row})
            row_num += 1
        for key, value in data_dict.items():
            if key == 0:
                header_list.append(value)
            else:
                print(value)
                id = value[0]
                order_reference = value[1]
                status = value[2]

                search_sale_order = self.env["sale.order"].search([('custom_so_id', '=', id)])

                if search_sale_order:
                    search_sale_order.write({'state': status})