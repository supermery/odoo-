# -*- coding: utf-8 -*-

from odoo import fields, models, api

class HrExpenseSheet(models.Model):

    _inherit = 'hr.expense.sheet'

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
                                  'Expense sheet and in the Operating Unit '
                                  'must be the same.'))