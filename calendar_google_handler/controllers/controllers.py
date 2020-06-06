# -*- coding: utf-8 -*-
# from odoo import http


# class GoogleCalHandler(http.Controller):
#     @http.route('/calendar_google_handler/calendar_google_handler/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/calendar_google_handler/calendar_google_handler/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('calendar_google_handler.listing', {
#             'root': '/calendar_google_handler/calendar_google_handler',
#             'objects': http.request.env['calendar_google_handler.calendar_google_handler'].search([]),
#         })

#     @http.route('/calendar_google_handler/calendar_google_handler/objects/<model("calendar_google_handler.calendar_google_handler"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('calendar_google_handler.object', {
#             'object': obj
#         })
