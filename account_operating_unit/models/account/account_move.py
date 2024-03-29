# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    operating_unit_id = fields.Many2one(
    	comodel_name='operating.unit',
        string='Default operating unit',
        help="This operating unit will "
            "be defaulted in the move lines."
    )

    @api.multi
    def _prepare_inter_ou_balancing_move_line(self, move, ou_id,
                                              ou_balances):
        if not move.company_id.inter_ou_clearing_account_id:
            raise UserError(_('Error!\nYou need to define an inter-operating\
                unit clearing account in the company settings'))

        res = {
            'name': 'OU-Balancing',
            'move_id': move.id,
            'journal_id': move.journal_id.id,
            'date': move.date,
            'operating_unit_id': ou_id,
            'account_id': move.company_id.inter_ou_clearing_account_id.id
        }

        if ou_balances[ou_id] < 0.0:
            res['debit'] = abs(ou_balances[ou_id])
        else:
            res['credit'] = ou_balances[ou_id]
        return res

    @api.multi
    def _check_ou_balance(self, move):
        # Look for the balance of each OU
        ou_balance = {}
        for line in move.line_ids:
            if line.operating_unit_id.id not in ou_balance:
                ou_balance[line.operating_unit_id.id] = 0.0
            ou_balance[line.operating_unit_id.id] += (line.debit - line.credit)
        return ou_balance

    @api.multi
    def post(self, invoice=False):
        ml_obj = self.env['account.move.line']
        for move in self:
            if not move.company_id.ou_is_self_balanced:
                continue

            # If all move lines point to the same operating unit, there's no
            # need to create a balancing move line
            ou_list_ids = [line.operating_unit_id and
                           line.operating_unit_id.id for line in
                           move.line_ids if line.operating_unit_id]
            if len(ou_list_ids) <= 1:
                continue

            # Create balancing entries for un-balanced OU's.
            ou_balances = self._check_ou_balance(move)
            amls = []
            for ou_id in list(ou_balances.keys()):
                # If the OU is already balanced, then do not continue
                if move.company_id.currency_id.is_zero(ou_balances[ou_id]):
                    continue
                # Create a balancing move line in the operating unit
                # clearing account
                line_data = self._prepare_inter_ou_balancing_move_line(
                    move, ou_id, ou_balances)
                if line_data:
                    amls.append(ml_obj.with_context(wip=True).
                                create(line_data))
            if amls:
                move.with_context(wip=False).\
                    write({'line_ids': [(4, aml.id) for aml in amls]})

        return super(AccountMove, self).post(invoice)

    def assert_balanced(self):
        if self.env.context.get('wip'):
            return True
        return super(AccountMove, self).assert_balanced()

    @api.multi
    @api.constrains('line_ids')
    def _check_ou(self):
        for move in self:
            if not move.company_id.ou_is_self_balanced:
                continue
            for line in move.line_ids:
                if not line.operating_unit_id:
                    raise UserError(_('Configuration error!\nThe operating\
                    unit must be completed for each line if the operating\
                    unit has been defined as self-balanced at company level.'))
