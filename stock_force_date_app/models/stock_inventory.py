# -*- coding: utf-8 -*-
import datetime
import time
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_repr, float_round


class InventoryAdjustment(models.Model):
	_inherit = 'stock.quant'

	force_date = fields.Datetime(string="Force Date")

	@api.model
	def create(self, values):
		force_date = self._context.get('force_date')
		res = super(InventoryAdjustment, self).create(values)
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date') and force_date:
			self.env.cr.execute("""update stock_quant set create_date=%s where id=%s""", (force_date, res.id))
		return res

	def write(self, values):
		force_date = self._context.get('force_date')
		res = super(InventoryAdjustment, self).write(values)
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date') and force_date:
			self.env.cr.execute("""update stock_quant set write_date=%s, create_date=%s where id=%s""", (force_date, force_date, self.id))
		return res


class StockPicking(models.Model):
	_inherit = 'stock.picking'

	force_date = fields.Datetime(string="Force Date")

	# Cj
	@api.onchange('force_date')
	def _verify_force_date(self):
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			if self.force_date and self.date_deadline:
				if self.force_date.date() != self.date_deadline.date():
					raise ValidationError(_('Force date and deadline date should be same.'))

	@api.constrains('force_date')
	def _check_force_date(self):
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			if self.force_date and self.date_deadline:
				if self.force_date.date() != self.date_deadline.date():
					raise ValidationError(_('Force date and deadline date should be same.'))

	def button_validate(self):
		#  Check Point: Here if the user has entered Back Date Quotation date from sale order or Receipt date from
		#  Purchase Order and didn't insert Force Date on Transfer Page It will raise Validation Error
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			if self.date_deadline and not self.force_date and self.date_deadline.date() != datetime.date.today():
				raise ValidationError(_('Please Enter Force Date as Deadline Date is of {}').format(self.date_deadline))
		res = super(StockPicking, self.with_context(force_date=self.force_date)).button_validate()
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			if self.force_date:
				# Overriding Effective Date to force date on successful validation
				self.write({'date_done': self.force_date})
				for move_ids in self.move_ids_without_package:
					self._cr.execute("""update stock_move set write_date=%s, create_date=%s where id=%s""",
									 (str(self.force_date), str(self.force_date), move_ids.id))
				for move_line_ids in self.move_line_ids_without_package:
					self._cr.execute("""update stock_move set write_date=%s, create_date=%s where id=%s""",
									 (str(self.force_date), str(self.force_date), move_line_ids.id))

		return res
	# End Cj


class StockMove(models.Model):
	_inherit = 'stock.move'

	def _action_done(self, cancel_backorder=False):
		force_date = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			for move in self:
				if move.picking_id:
					if move.picking_id.force_date:
						force_date = move.picking_id.force_date
					else:
						force_date = move.picking_id.scheduled_date
		res = super(StockMove, self)._action_done()
		if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
			if force_date:
				for move in res:
					move.write({'date': force_date})
					if move.move_line_ids:
						for move_line in move.move_line_ids:
							move_line.write({'date': force_date})
					# CJ
					# Overriding Create Date of Stock.Valuation.Layer
					if move.picking_id.force_date:
						valuation = move.stock_valuation_layer_ids
						if valuation:
							for line in valuation:
								self.env.cr.execute("""UPDATE stock_valuation_layer SET create_date=%s WHERE id=%s""", (force_date, line.id))
					# End CJ
		return res

	def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):
		self.ensure_one()
		AccountMove = self.env['account.move'].with_context(default_journal_id=journal_id)
		move_lines = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description)
		if move_lines:
			date = self._context.get('force_period_date', fields.Date.context_today(self))
			if self.env.user.has_group('stock_force_date_app.group_stock_force_date'):
				if self.picking_id.force_date:
					date = self.picking_id.force_date.date()
			new_account_move = AccountMove.sudo().create({
				'journal_id': journal_id,
				'line_ids': move_lines,
				'date': date,
				'ref': description,
				'stock_move_id': self.id,
				'stock_valuation_layer_ids': [(6, None, [svl_id])],
				'move_type': 'entry',
			})
			new_account_move._post()
