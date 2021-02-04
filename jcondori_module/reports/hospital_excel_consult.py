from odoo.tools.misc import xlsxwriter
from odoo import api, models, fields
from odoo.osv import expression
import base64
import io


class HospitalExcelConsult(models.TransientModel):
    _name = 'hospital.excel_consult_modal'
    _description = 'Hospital Excel Consults'

    name = fields.Date('Date')
    category_id = fields.Many2one('hospital.category', string='Category')

    state = fields.Selection([('new', 'New'), ('finish', 'Finish')], string='State', default='new')

    file = fields.Binary('File')
    file_name = fields.Char('File Name')

    def generate_excel(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        domain = []
        if self.name:
            domain = expression.AND([domain, [('date', '=', fields.Date.to_string(self.name))]])
        if self.category_id:
            domain = expression.AND([domain, [('category_id', '=', self.category_id.id)]])
        consults = self.env['hospital.consult'].search(domain)

        # Formatos / Estilos
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        merge_format = workbook.add_format({'align': 'center', 'bold': True})

        # Ancho de Columnas
        worksheet.set_column(0, 0, 3)  # A
        worksheet.set_column(1, 1, 17)  # B
        worksheet.set_column(3, 3, 17)  # C
        worksheet.set_column(4, 4, 17)  # E

        # Cabezera
        worksheet.merge_range('B2:E2', 'Patient', merge_format)

        # Sub Cabezeras
        worksheet.write_string('B3', 'Name')
        worksheet.write_string('C3', 'Patient')
        worksheet.write_string('D3', 'Date')
        worksheet.write_string('E3', 'Category')

        row = 3
        for consult in consults:
            worksheet.write_string(row, 1, consult.name)
            worksheet.write_string(row, 2, consult.patient_id.name)
            worksheet.write_datetime(row, 3, consult.date, date_format)
            worksheet.write_string(row, 4, consult.category_id.name)
            row += 1  # row = row + 1

        workbook.close()
        output.seek(0)

        self.write({
            'file': base64.b64encode(output.getvalue()),
            'file_name': 'prueba.xlsx',
            'state': 'finish',
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Hospital Excel Consult',
            'res_model': 'hospital.excel_consult_modal',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new'
        }
