# -*- coding: utf-8 -*-
from werkzeug.exceptions import NotFound

import odoo.http as http
from odoo import fields
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import PPG, TableCompute, PPR
from odoo.http import request
import json
