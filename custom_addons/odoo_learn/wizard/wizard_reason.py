from odoo import fields, models, api


class WizardReason(models.TransientModel):
    _name = 'reason.wizard'
    _description = 'Description'

    reason = fields.Text(string="Reason")


    def action_confirm(self):
       temp = self.env.context.get('active_id', False)
       modern = self.env['learn.modern'].browse(temp)
       modern.write({'reason': self.reason})
       modern.To_leave()