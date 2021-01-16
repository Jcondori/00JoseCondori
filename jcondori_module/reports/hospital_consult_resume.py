from odoo import api, models, fields


class HospitalConsultResumeModal(models.TransientModel):
    _name = 'hospital.consult_resume_modal'
    _description = 'Hospital Consult Resume Modal'

    name = fields.Date('Date')


class HospitalConsultResume(models.AbstractModel):
    _name = 'report.jcondori_module.hospital_consult_resume'
    _description = 'Hospital Consult Resume'

    @api.model
    def _get_report_values(self, docids, data=None):
        patients = []
        query_str = """select hp.name, count(hp.name)
                        from hospital_consult hc
                        inner join hospital_patient hp on hc.patient_id = hp.id
                        group by hp.name
                    """
        self.env.cr.execute(query_str)
        for patient, count in self.env.cr.fetchall():
            patients.append({'patient_name': patient,
                             'patient_count': count})
        data = {'name': 'Prueba',
                'note': 'Funcionó',
                'patients': patients}
        return data
