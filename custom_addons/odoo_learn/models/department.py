from odoo import fields, models, api
from datetime import date
import random
class Department(models.Model):
    _name = 'learn.department'
    _description = 'learning department'

    name = fields.Char()
    description = fields.Text()
    modern_ids = fields.One2many(comodel_name='learn.modern', inverse_name='department',string="Modern")
    modern_count = fields.Integer(string="modern count", compute="get_count_modern", store=True)
    age = fields.Date(string="Day of Birth")
    @api.depends('modern_ids')
    def get_count_modern(self):
        for temp in self:
            temp.modern_count = len(temp.modern_ids)


    def create_modern(self):
        self.ensure_one()
        name_ran = ['Truong', 'Lan', 'Hao', 'Hoa']
        random_choice = random.choice(name_ran)
        create_modern = {
            'name': random_choice,
            'phone': '09123131234',
            'department': self.id,
        }
        self.env['learn.modern'].create(create_modern)

    