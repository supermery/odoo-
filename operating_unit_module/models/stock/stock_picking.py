# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"

    operating_unit_id = fields.Many2one(
    	comodel_name='operating.unit',
        string='Requesting Operating Unit',        
        default=lambda self:self.env['res.users'].operating_unit_default_get(self._uid),
    )

    @api.onchange('picking_type_id', 'partner_id')
    def onchange_picking_type(self):
        res = super(StockPicking, self).onchange_picking_type()
        if self.picking_type_id:
            self.operating_unit_id = self.picking_type_id.warehouse_id.operating_unit_id
        return res

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and
                    rec.company_id != rec.operating_unit_id.company_id):
                raise UserError(
                    _('Configuration error\nThe Company in the Stock Picking '
                      'and in the Operating Unit must be the same.')
                )

    @api.multi
    @api.constrains('operating_unit_id', 'picking_type_id')
    def _check_picking_type_operating_unit(self):
        for rec in self:
            warehouse = rec.picking_type_id.warehouse_id
            if (rec.picking_type_id and rec.operating_unit_id and
                    warehouse.operating_unit_id != rec.operating_unit_id):
                raise UserError(
                    _('Configuration error\nThe Operating Unit of the picking '
                      'must be the same as that of the warehouse of the '
                      'Picking Type.')
                )