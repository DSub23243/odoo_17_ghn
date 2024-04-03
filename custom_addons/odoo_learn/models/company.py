from odoo import fields, models, api


class Company(models.Model):
    _name = 'learn.company'
    _description = 'learning for company'

    name = fields.Char()
    modern_ids = fields.Many2many(comodel_name="learn.modern", relation="company_rel", column1="company_id", column2="modern_id", string="modern")

    code = fields.Char(string="Code", readonly=True)

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('company.seq')
        return super(Company,self).create(vals)