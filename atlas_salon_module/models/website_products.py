from odoo import api, fields, models, _


class ProductWebsite(models.Model):

    _inherit = 'product.template'

    operating_unit = fields.Many2one ( comodel_name='operating.unit', string='Operating Unit')



