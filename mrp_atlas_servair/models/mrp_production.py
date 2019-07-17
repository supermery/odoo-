# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime


class MrpProduction(models.Model):

    _inherit = 'mrp.production'
    
    date_fin = fields.Datetime(string="Date prévu")
    mrp_estimation_ids = fields.One2many(comodel_name="mrp.production.workcenter.estimation", inverse_name="production_id", string="Plannification")
    
    
    @api.multi
    def button_plan(self):
        res = super(MrpProduction, self).button_plan()
        for mo in self:
            for operation in mo.routing_id.mapped('operation_ids'):
                self.env['mrp.production.workcenter.estimation'].create({'name': operation.name,
                                                                         'workcenter_id': operation.workcenter_id.id,
                                                                         'production_id': self.id})
        
class MrpProductionWorkcenterEstimation(models.Model):
    
    _name = 'mrp.production.workcenter.estimation'
    
    name = fields.Char(string="Opération")
    workcenter_id = fields.Many2one(comodel_name="mrp.workcenter", string="Poste de travail")
    nbr_ressources_prevu = fields.Integer(string="Nombre de ressources prévu", compute="_get_nbr_jours")
    production_id = fields.Many2one(comodel_name="mrp.production", string="Ordre de fabrication")
    
    @api.multi
    def _get_nbr_jours(self):
        for mo in self:
            if mo.production_id.date_fin:
                cmpt = datetime.strptime(
                                mo.production_id.date_fin, '%Y-%m-%d %H:%M:%S').date() - datetime.strptime(
                                mo.production_id.date_planned_start, '%Y-%m-%d %H:%M:%S').date()
                
                estimated_duration = mo.production_id.routing_id.mapped('operation_ids').filtered(lambda r: r.name == mo.name).time_cycle_manual * mo.production_id.product_qty
                mo.nbr_ressources_prevu = (cmpt.days * 7 / estimated_duration) + 1
