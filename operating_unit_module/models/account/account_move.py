# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):

    _inherit = 'account.move'

    @api.multi
    @api.constrains('operating_unit_id')
    def check_payslips_ou(self):
        for move in self:
            pay = self.env['hr.payslip'].search(
                [('move_id', '=', move.id)])
            if ((pay.operating_unit_id and move.operating_unit_id)
                    and (pay.operating_unit_id != move.operating_unit_id)):
                raise ValidationError(_(
                    'The journal entry and the payslip must have same '
                    'operating unit'))
        return True