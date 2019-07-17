# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    operating_unit_id = fields.Many2one(
    	comodel_name='operating.unit', 
    	string='Operating Unit'
    )

    @api.model
    def create(self, vals):
        if vals.get('move_id', False):
            move = self.env['account.move'].browse(vals['move_id'])
            if move.operating_unit_id:
                vals['operating_unit_id'] = move.operating_unit_id.id
        return super(AccountMoveLine, self).create(vals)

    @api.model
    def _query_get(self, domain=None):
        if domain is None:
            domain = []
        if self._context.get('operating_unit_ids', False):
            domain.append(('operating_unit_id', 'in',
                           self._context.get('operating_unit_ids')))
        return super(AccountMoveLine, self)._query_get(domain)

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and rec.company_id !=
                    rec.operating_unit_id.company_id):
                raise UserError(_('Configuration error!\nThe Company in the'
                                  ' Move Line and in the Operating Unit must '
                                  'be the same.'))

    @api.multi
    @api.constrains('operating_unit_id', 'move_id')
    def _check_move_operating_unit(self):
        for rec in self:
            if (rec.move_id and rec.move_id.operating_unit_id and
                rec.operating_unit_id and rec.move_id.operating_unit_id !=
                    rec.operating_unit_id):
                raise UserError(_('Configuration error!\nThe Operating Unit in'
                                  ' the Move Line and in the Move must be the'
                                  ' same.'))
