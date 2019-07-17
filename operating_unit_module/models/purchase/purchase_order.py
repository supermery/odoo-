# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        states={'draft': [('readonly', False)]},
        default=lambda self: (self.env['res.users'].
                              operating_unit_default_get(self.env.uid))
    )

    @api.constrains(
        'operating_unit_id', 
        'requesting_operating_unit_id',
        'company_id'
    )
    def _check_company_operating_unit(self):
        for record in self:
            if (record.company_id and record.operating_unit_id and
                    record.company_id != record.operating_unit_id.company_id):
                raise ValidationError(
                    _('Configuration error\nThe Company in the Purchase Order '
                      'and in the Operating Unit must be the same.'))