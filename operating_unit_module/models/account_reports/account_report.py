# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from datetime import datetime, timedelta
from odoo.addons.web.controllers.main import clean_action
from odoo.tools import float_is_zero

class AccountReport(models.AbstractModel):
    _inherit = 'account.report'

    filter_operatings = True
    show_operating_filter = fields.Boolean('Allow filtering by Operatings Units', help='display the operating filter in the report')

    @api.model
    def get_options(self, previous_options=None):
        res = super(AccountReport,self).get_options(previous_options)
        if self.show_operating_filter:
            self.filter_operatings = True
        return res
    
    def _build_options(self, previous_options=None):
        res = super(AccountReport,self)._build_options(previous_options)
        res['operatings'] = self.get_operatings()
        return res

    def get_templates(self):
        res = super(AccountReport,self).get_templates()
        res['main_template'] = 'operating_unit_module.main_template_inherit'
        return res

    def _get_filter_operatings(self):
        return self.env['operating.unit'].search([('company_id', 'in', self.env.user.company_ids.ids or [self.env.user.company_id.id])], order="company_id, name")

    def get_operatings(self):
        operatings_read = self._get_filter_operatings()
        operatings = []
        previous_company = False
        for opp in operatings_read:
            if opp.company_id != previous_company:
                operatings.append({'id': 'divider', 'name': opp.company_id.name})
                previous_company = opp.company_id
        for opp in operatings_read:
            operatings.append({'id': opp.id, 'name': opp.name, 'code': opp.code,'selected': False})
        return operatings

    def set_context(self, options):
        """This method will set information inside the context based on the options dict as some options need to be in context for the query_get method defined in account_move_line"""
        ctx = self.env.context.copy()
        if options.get('cash_basis'):
            ctx['cash_basis'] = True
        if options.get('date') and options['date'].get('date_from'):
            ctx['date_from'] = options['date']['date_from']
        if options.get('date'):
            ctx['date_to'] = options['date'].get('date_to') or options['date'].get('date')
        if options.get('all_entries') is not None:
            ctx['state'] = options.get('all_entries') and 'all' or 'posted'
        if options.get('journals'):
            ctx['journal_ids'] = [j.get('id') for j in options.get('journals') if j.get('selected')]
        company_ids = []
        if options.get('multi_company'):
            company_ids = [c.get('id') for c in options['multi_company'] if c.get('selected')]
            company_ids = company_ids if len(company_ids) > 0 else [c.get('id') for c in options['multi_company']]
        ctx['company_ids'] = len(company_ids) > 0 and company_ids or [self.env.user.company_id.id]
        if options.get('analytic_accounts'):
            ctx['analytic_account_ids'] = self.env['account.analytic.account'].browse([int(acc) for acc in options['analytic_accounts']])
        if options.get('analytic_tags'):
            ctx['analytic_tag_ids'] = self.env['account.analytic.tag'].browse([int(t) for t in options['analytic_tags']])
        ctx['operating_unit_ids'] = [opp.get('id') for opp in options.get('operatings') if opp.get('selected')]
        return ctx