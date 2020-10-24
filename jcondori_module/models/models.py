# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(string='Name')
    surname = fields.Char(string='Surname')
    birthdate = fields.Date(string='Birthdate')
