# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit', 
        String='Operating Unit',
        default=lambda self:self.env['res.users'].operating_unit_default_get(self._uid),
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]}
    )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and
                    rec.company_id != rec.operating_unit_id.company_id):
                raise ValidationError(_('Configuration error\nThe Company in'
                                        ' the Sales Order and in the Operating'
                                        ' Unit must be the same.'))

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['operating_unit_id'] = self.operating_unit_id.id
        return invoice_vals