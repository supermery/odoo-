# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError

class HrContract(models.Model):

    _inherit = 'hr.contract'

    operating_unit_id = fields.Many2one(
    	comodel_name='operating.unit', 
    	string='Operating Unit',
        default=lambda self:self.env['res.users'].operating_unit_default_get(self._uid)
    )