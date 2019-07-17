# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    operating_unit_id = fields.Many2one(
    	comodel_name='operating.unit',
        related='invoice_id.operating_unit_id',
        string='Operating Unit', 
        store=True,
        readonly=True
    )