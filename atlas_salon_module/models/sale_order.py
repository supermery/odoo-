from odoo import api, fields, models, _
from odoo.addons.website.models.website import Website


class SaleOrder(models.Model):
    _inherit = 'sale.order'



    is_salon_so = fields.Boolean(string="Is Salon SO")
    as_salon_id = fields.Many2one(comodel_name='as.salon', string='Salon', index=True)
    operating_unit = fields.Many2one(comodel_name='operating.unit', string='Operating Unit')

    @api.onchange('as_salon_id')
    def onchange_as_salon_id(self):
        self.operating_unit = self.as_salon_id.operating_unit.id
        self.partner_id = self.as_salon_id.partner_id.id

class Website(models.Model):
    _inherit = 'website'

    @api.multi
    def _prepare_sale_order_values(self, partner, pricelist):
        values = super(Website, self)._prepare_sale_order_values(partner, pricelist)
        values.update({
            'is_salon_so': True,
            'as_salon_id': 1,
            'operating_unit':2,
        })
        return values


