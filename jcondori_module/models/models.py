# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(string='Name', required=True)
    surname = fields.Char(string='Surname', required=True)
    birthdate = fields.Date(string='Birthdate')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    is_adult = fields.Boolean(string='Is Adult')
    number_consults = fields.Integer(string='Nomber Consults', readonly=True)

    partner_id = fields.Many2one(comodel_name='res.partner', string='Patient Contact')
    mobile = fields.Char(string='Mobile', related='partner_id.mobile', store=True)

    @api.constrains('birthdate')
    def _check_birthdate(self):
        for rec in self:
            if rec.birthdate > fields.Date.today():
                raise ValidationError('The date of birth cannot be older than the current date')

    @api.depends('birthdate')
    def _compute_age(self):
        for rec in self:
            edad = 0
            if rec.birthdate:
                edad = fields.Date.today().year - rec.birthdate.year
            rec.age = edad

    @api.onchange('birthdate')
    def _onchange_birthdate(self):
        for rec in self:
            is_adult = False
            edad = 0
            if rec.birthdate:
                edad = fields.Date.today().year - rec.birthdate.year
            if edad > 18:
                is_adult = True
            rec.is_adult = is_adult

    def consult_finish(self):
        for rec in self:
            rec.number_consults += 1
            rec.birthdate = fields.Date.today()

    @api.model
    def update_ruc(self):
        patients = self.env['hospital.patient'].search([])
        for rec in patients:
            rec.cosulta_ruc()

    def save_quantity_patinent(self):
        for rec in self:
            #Logica
            True
