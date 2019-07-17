# -*- coding: utf-8 -*-

from odoo import fields, models

class SaleReport(models.Model):

    _inherit = "sale.report"

    # operating_unit_id = fields.Many2one(
    #     comodel_name='operating.unit', 
    #     string='Operating Unit'
    # )

    # def _select(self):
    #     select_str = super(SaleReport, self)._select()
    #     select_str += """
    #         ,s.operating_unit_id
    #     """
    #     print('select_str',select_str)
    #     return select_str

    # def _group_by(self):
    #     group_by_str = super(SaleReport, self)._group_by()
    #     group_by_str += """
    #         ,s.operating_unit_id
    #     """
    #     return group_by_str