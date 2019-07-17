# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = "stock.move"

    operating_unit_id = fields.Many2one(
        related='location_id.operating_unit_id',
        string='Source Location Operating Unit',
        readonly=True,
    )
    operating_unit_dest_id = fields.Many2one(
        related='location_dest_id.operating_unit_id',
        string='Dest. Location Operating Unit',
        readonly=True,
    )

    @api.multi
    @api.constrains('operating_unit_id', 'picking_id',
                    'location_id', 'operating_unit_dest_id',
                    'location_dest_id')
    def _check_stock_move_operating_unit(self):
        for stock_move in self:
            if not stock_move.operating_unit_id:
                return True
            operating_unit = stock_move.operating_unit_id
            operating_unit_dest = stock_move.operating_unit_dest_id
            if (stock_move.location_id and
                stock_move.location_id.operating_unit_id and
                stock_move.picking_id and
                operating_unit != stock_move.picking_id.operating_unit_id
                ) and (
                stock_move.location_dest_id and
                stock_move.location_dest_id.operating_unit_id and
                stock_move.picking_id and
                operating_unit_dest != stock_move.picking_id.operating_unit_id
            ):
                raise UserError(
                    _('Configuration error\nThe Stock moves must '
                      'be related to a location (source or destination) '
                      'that belongs to the requesting Operating Unit.')
                )

    @api.model
    def _prepare_account_move_line(self, qty, cost, credit_account_id,
                                   debit_account_id):
        res = super(StockMove, self)._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id)
        if res:
            debit_line_vals = res[0][2]
            credit_line_vals = res[1][2]

            if (
                self.operating_unit_id and self.operating_unit_dest_id and
                self.operating_unit_id != self.operating_unit_dest_id and
                debit_line_vals['account_id'] != credit_line_vals['account_id']
            ):
                raise exceptions.UserError(
                    _('You cannot create stock moves involving separate source'
                      ' and destination accounts related to different '
                      'operating units.')
                )

            debit_line_vals['operating_unit_id'] = (
                self.operating_unit_dest_id.id or self.operating_unit_id.id
            )
            credit_line_vals['operating_unit_id'] = (
                self.operating_unit_id.id or self.operating_unit_dest_id.id
            )
            return [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
        return res