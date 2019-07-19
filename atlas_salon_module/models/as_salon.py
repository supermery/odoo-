# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AsSalon ( models.Model ):
    _name = 'as.salon'

    name = fields.Char ( string="Salon's name", required="True" )
    note = fields.Text ( string="Note" )
    operating_unit = fields.Many2one ( comodel_name='operating.unit', string='Operating Unit' )
    active = fields.Boolean ( string="Exposed on portail" )
    allowed_users_ids = fields.Many2many ( 'res.users', string="Allowed Users" )
    partner_id = fields.Many2one ( 'res.partner', string="Client" )
