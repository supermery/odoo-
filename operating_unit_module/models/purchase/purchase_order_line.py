# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    operating_unit_id = fields.Many2one(
    	related='order_id.operating_unit_id',
        string='Operating Unit',
        readonly=True
    )
