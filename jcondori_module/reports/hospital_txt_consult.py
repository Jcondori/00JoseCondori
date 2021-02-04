from odoo import api, models, fields
from odoo.osv import expression
import base64



class HospitalTxtConsult(models.TransientModel):
    _name = 'hospital.txt_consult_modal'
    _description = 'Hospital TXT Consults'

    name = fields.Date('Date')
    category_id = fields.Many2one('hospital.category', string='Category')

    state = fields.Selection([('new', 'New'), ('finish', 'Finish')], string='State', default='new')

    file = fields.Binary('File')
    file_name = fields.Char('File Name')

    def generate_txt(self):
        txt_content = ''
        domain = []
        if self.name:
            domain = expression.AND([domain, [('date', '=', fields.Date.to_string(self.name))]])
        if self.category_id:
            domain = expression.AND([domain, [('category_id', '=', self.category_id.id)]])
        consults = self.env['hospital.consult'].search(domain)
        for consult in consults:
            txt_line = '%s|%s|%s|%s' % (
                consult.name or '',
                fields.Date.to_string(consult.date) if consult.date else '',
                consult.patient_id.name if consult.patient_id else '',
                consult.category_id.name if consult.category_id else ''
            )
            txt_content += txt_line + '\n'

        self.write({
            'file': base64.b64encode(txt_content.encode('utf-8')),
            'file_name': 'prueba.txt',
            'state': 'finish',
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Hospital TXT Consult',
            'res_model': 'hospital.txt_consult_modal',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new'
        }
