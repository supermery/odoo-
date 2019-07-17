# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    operating_unit_id = fields.Many2one(
    	comodel_name='operating.unit',
        related='order_id.operating_unit_id',
        string='Operating Unit', 
        store=True,
        readonly=True,
    )

    analytic_account_id = fields.Many2one(
    	comodel_name='account.analytic.account', 
    	string='Business Units', 
    	readonly=True, 
    	states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, 
    	help="The analytic account related to a sales order Line.", 
    	copy=False
    )

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update({'account_analytic_id': self.analytic_account_id.id})
        return res