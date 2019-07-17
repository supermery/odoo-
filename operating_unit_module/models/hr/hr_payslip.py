# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError

class HrPayslip(models.Model):

    _inherit = 'hr.payslip'

    operating_unit_id = fields.Many2one(
        related='contract_id.operating_unit_id'
    )


    @api.multi
    def write(self, vals):
        res = super(HrPayslip, self).write(vals)
        if vals.get('move_id', False):
            for slip in self:
                if slip.operating_unit_id:
                    slip.move_id.operating_unit_id = slip.operating_unit_id.id
                    if slip.move_id.line_ids:
                        slip.move_id.line_ids.\
                            write({'operating_unit_id':
                                   slip.operating_unit_id.id})
        return res