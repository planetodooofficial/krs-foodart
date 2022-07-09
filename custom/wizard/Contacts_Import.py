from odoo import api, fields, models
import csv
import io, base64
from tempfile import TemporaryFile
import logging

_logger = logging.getLogger(__name__)


class CustomerWizard(models.TransientModel):
    _name = "customer.wizard"
    _description = "Customer Wizard"

    load_file = fields.Binary("Load File")

    def import_customer_data(self):
        print("Import is working")
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
                # name = value[0]
                # id = value[1]
                # banks_name = value[2]
                # banks_account_number = value[3]
                #
                # search_customer = self.env['res.partner'].search([('name', '=', name), ('id_custom', '=', id)])
                #
                # bank_id = self.env['res.partner.bank'].search([('bank_id', '=', banks_name)], limit=1).id
                #
                # if not bank_id:
                #     bank_account_val = {
                #         'name': banks_name,
                #     }
                #     bank_id = self.env['res.bank'].create(bank_account_val)
                # banks_val = (0, 0, {
                #     'bank_id': bank_id.id,
                #     'acc_number': banks_account_number,
                # })
                # if search_customer:
                #     search_customer.write(banks_val)
                company_type = value[0].strip()
                name = value[1].strip()
                id = value[2].strip()
                internal_reference = value[3].strip()
                street = value[4].strip()
                street2 = value[5].strip()
                city = value[6].strip()
                state = value[7].strip()
                zip = value[8].strip()
                country = value[9].strip()
                tax_id = value[10].strip()
                phone = value[11].strip()
                mobile = value[12].strip()
                email = value[13].strip()
                website = value[14].strip()
                language = value[15].strip()
                tags = value[16].strip()
                created_by = value[17].strip().strip()
                is_a_customer = value[18].strip()
                sales_person = value[19].strip()
                delivery_method = value[20].strip()
                bounce = value[21].strip()
                price_list = value[22].strip()
                is_a_vendor = value[23].strip()
                supplier_currency = value[24].strip()
                barcode = value[25].strip() or False
                company = value[26].strip()
                fiscal_position = value[27].strip()
                customer_location = value[28].strip()
                vendor_location = value[29].strip()
                account_receivable = value[30].strip()
                account_payable = value[31].strip()
                credit_limit = value[32].strip()
                related_company = value[33].strip()
                customer_payment_terms = value[34].strip()
                vendor_payment_terms = value[35].strip()
                customer_rank = value[36].strip()
                supplier_rank = value[37].strip()
                active = value[38].strip()

                state_id = self.env['res.country.state'].search([('name', '=', state)], limit=1)
                country_id = self.env['res.country'].search([('name', '=', country)], limit=1)
                category_id = self.env['res.partner.category'].search([('name', '=', tags)], limit=1)
                create_uid = self.env['res.users'].search([('name', '=', created_by), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                user_id = self.env['res.users'].search([('name', '=', sales_person), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                property_delivery_carrier_id = self.env['delivery.carrier'].search([('name', '=', delivery_method)], limit=1)
                property_product_pricelist_id = self.env['product.pricelist'].search([('name', '=', price_list)], limit=1)
                property_purchase_currency_id = self.env['res.currency'].search([('name', '=', supplier_currency)], limit=1)
                company_id = self.env['res.company'].search([('name', '=', company)], limit=1)
                property_account_position_id = self.env['account.fiscal.position'].search([('name', '=', fiscal_position)], limit=1)
                property_stock_customer_id = self.env['stock.location'].search([('name', '=', customer_location)], limit=1)
                property_stock_supplier_id = self.env['stock.location'].search([('name', '=', vendor_location)], limit=1)
                property_account_receivable_id = self.env['account.account'].search([('name', '=', account_receivable)], limit=1)
                property_account_payable_id = self.env['account.account'].search([('name', '=', account_payable)], limit=1)
                parent_id = self.env['res.partner'].search([('name', '=', related_company), '|', ('active', '=', True), ('active', '=', False)], limit=1)
                property_payment_term_id = self.env['account.payment.term'].search([('name', '=', customer_payment_terms)], limit=1)
                property_supplier_payment_term_id = self.env['account.payment.term'].search([('name', '=', vendor_payment_terms)], limit=1)

                contacts_val = {
                    'company_type': company_type,
                    'name': name if name else "No Name",
                    'custom_id': id,
                    'ref': internal_reference,
                    'street': street,
                    'street2': street2,
                    'city': city,
                    'state_id': state_id.id,
                    'zip': zip,
                    'country_id': country_id.id,
                    'vat': tax_id,
                    'phone': phone,
                    'mobile': mobile,
                    'email': email,
                    'website': website,
                    'lang': language,
                    'category_id': [(4, category_id.id)],
                    'create_uid': create_uid.id,
                    'created_by_custom': create_uid.id,
                    'is_customer': True if is_a_customer == "True" else False,
                    'user_id': user_id.id,
                    'property_delivery_carrier_id': property_delivery_carrier_id.id,  # make this field
                    'message_bounce': bounce,
                    'property_product_pricelist': property_product_pricelist_id.id,
                    'is_vendor': True if is_a_vendor == "True" else False,
                    'property_purchase_currency_id': property_purchase_currency_id.id,
                    'barcode': barcode,
                    'company_id': company_id.id,
                    'property_account_position_id': property_account_position_id.id,
                    'property_stock_customer': property_stock_customer_id.id,
                    'property_stock_supplier': property_stock_supplier_id.id,
                    'property_account_receivable_id': property_account_receivable_id.id,
                    'property_account_payable_id': property_account_payable_id.id,
                    'credit_limit': credit_limit,
                    'parent_id': parent_id.id,
                    'property_payment_term_id': property_payment_term_id.id,
                    'property_supplier_payment_term_id': property_supplier_payment_term_id.id,
                    'customer_rank': customer_rank,
                    'supplier_rank': supplier_rank,
                    'active': True if active == "True" else False,
                }
                contacts_obj_id = self.env['res.partner'].sudo().create(contacts_val)