# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, timedelta

class MrpBom(models.Model):

    _inherit = 'mrp.bom'
    is_salon_bom = fields.Boolean(string="Is Salon BOM")
