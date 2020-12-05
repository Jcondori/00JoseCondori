# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
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

    partner_id = fields.Many2one('res.partner', string='Patient Contact')
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


class HospitalCategory(models.Model):
    _name = 'hospital.category'
    _description = 'Hospital Category'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)


class HospitalConsult(models.Model):
    _name = 'hospital.consult'
    _description = 'Hospital Consult'

    name = fields.Char(string='Name', required=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    date = fields.Date(required=True, default=fields.Date.context_today)
    diagnostic = fields.Html('Diagnostic')
    recipe = fields.Html('Recipe')
    category_id = fields.Many2one('hospital.category', string='Category', required=True)

    def action_register_invoice(self):
        return {
            'name': _('Create Invoice'),
            'res_model': 'hospital.consult.invoice',
            'view_mode': 'form',
            'context': {
                'active_model': 'hospital.consult',
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }


class HospitalConsultInvoice(models.TransientModel):
    _name = 'hospital.consult.invoice'
    _description = 'Create Invoice Consult'

    journal_id = fields.Many2one('account.journal', string='Journal', required=True)

    def action_create_invoice(self):
        consults = self.env['hospital.consult'].browse(self._context.get('active_ids', []))
        for consult in consults:
            vals = {
                'journal_id': self.journal_id and self.journal_id.id or False,
                'partner_id': consult.patient_id.partner_id and consult.patient_id.partner_id.id or False,
                'move_type': 'out_invoice',
                'state': 'draft'
            }
            invoice = self.env['account.move'].create(vals)
            consult.invoice_id = invoice and invoice.id or False
