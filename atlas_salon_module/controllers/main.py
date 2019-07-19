# -*- coding: utf-8 -*-
from werkzeug.exceptions import NotFound

import odoo.http as http
from odoo import fields
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import PPG, TableCompute, PPR
from odoo.http import request
import json

class WebsiteSale(http.Controller):
    def _get_search_order(self, post):
        # OrderBy will be parsed in orm and so no direct sql injection
        # id is added to be sure that order is a unique sort key
        return 'website_published desc,%s , id desc' % post.get('order', 'website_sequence desc')

    def _get_compute_currency_and_context(self):
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)

        return compute_currency, pricelist_context, pricelist

    def _get_search_domain_by_salon(self, search, salon, attrib_values):
        domain = request.website.sale_product_domain()
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch)]

        if salon:
            domain += [('operating_unit', '=', int(salon.operating_unit))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]

        return domain

    @http.route([
        '/shop_by_salon',
        '/shop_by_salon/page/<int:page>',
        '/shop_by_salon/salon/<model("as.salon"):salon>',
        '/shop_by_salon/salon/<model("as.salon"):salon>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop_by_salon(self, page=0, salon=None, search='', ppg=False, **post):
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG
        
        if salon:
            salon = request.env['as.salon'].search([('id', '=', int(salon))], limit=1)
            if not salon:
                raise NotFound()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain_by_salon(search, salon, attrib_values)

        keep = QueryURL('/shop_by_salon', salon=salon and int(salon), search=search, attrib=attrib_list, order=post.get('order'))

        compute_currency, pricelist_context, pricelist = self._get_compute_currency_and_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop_by_salon"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        salons = request.env['as.salon'].search([])


        Product = request.env['product.template']

        parent_category_ids = []
        if salon:
            url = "/shop_by_salon/salon/%s" % slug(salon)


        product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttribute.search([('attribute_line_ids.product_tmpl_id', 'in', selected_products.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        values = {
            'search': search,
            'salon': salon,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'rows': PPR,
            'salons': salons,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
        }
        if salon:
            values['main_object'] = salon
        return request.render("website_sale.products", values)
