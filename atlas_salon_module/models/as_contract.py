from odoo import models, fields


class AsSalon ( models.Model ):
    _name = 'as.contract'

    num_contract = fields.Char ( string="Num Contract" )
    duration_from = fields.Date ( string="Duration De " )
    duration_to = fields.Date ( string="Duration A " )
