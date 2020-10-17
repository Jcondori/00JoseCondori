# -*- coding: utf-8 -*-
# from odoo import http


# class JcondoriModule(http.Controller):
#     @http.route('/jcondori_module/jcondori_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jcondori_module/jcondori_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('jcondori_module.listing', {
#             'root': '/jcondori_module/jcondori_module',
#             'objects': http.request.env['jcondori_module.jcondori_module'].search([]),
#         })

#     @http.route('/jcondori_module/jcondori_module/objects/<model("jcondori_module.jcondori_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jcondori_module.object', {
#             'object': obj
#         })
