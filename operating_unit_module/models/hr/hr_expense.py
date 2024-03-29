# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError

class HrExpense(models.Model):

    _inherit = 'hr.expense'

    operating_unit_id = fields.Many2one(
    	comodel_name='operating.unit', 
    	string='Operating Unit',
        default=lambda self:self.env['res.users'].operating_unit_default_get(self._uid)
    )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and rec.company_id !=
                    rec.operating_unit_id.company_id):
                raise UserError(_('Configuration error. The Company in the '
                                  'Expense and in the Operating Unit '
                                  'must be the same.'))

    @api.multi
    @api.constrains('operating_unit_id', 'sheet_id')
    def _check_expense_operating_unit(self):
        for rec in self:
            if (rec.sheet_id and rec.sheet_id.operating_unit_id and
                rec.operating_unit_id and rec.sheet_id.operating_unit_id !=
                    rec.operating_unit_id):
                raise UserError(_('Configuration error. The Operating Unit in'
                                  ' the Expense sheet and in the Expense must '
                                  'be the same.'))

    @api.multi
    def submit_expenses(self):
        res = super(HrExpenseExpense, self).submit_expenses()
        if len(self.mapped('operating_unit_id')) != 1 or\
                any(not expense.operating_unit_id for expense in self):
            raise UserError(_('You cannot submit the Expenses having'
                              ' different Operating Units or with'
                              ' no Operating Unit!'))
        if res.get('context'):
            res.get('context').\
                update({'default_operating_unit_id':
                        self[0].operating_unit_id.id})
        return res

    def _prepare_move_line(self, line):
        res = super(HrExpenseExpense, self)._prepare_move_line(line)
        res.update({'operating_unit_id': self.operating_unit_id.id})
        return res