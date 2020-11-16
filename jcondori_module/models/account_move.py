from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    sunat_serie = fields.Char(string='Sunat Serie', size=4)
    sunat_correlative = fields.Char(string='Sunat Correlative', size=10)
