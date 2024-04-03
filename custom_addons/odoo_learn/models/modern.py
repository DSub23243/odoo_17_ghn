from odoo import models, fields, api
from datetime import date
from odoo.exceptions import UserError

class Modern(models.Model):
    _name = "learn.modern"
    _description = "learning modern"

    name = fields.Char(string="Name", required=True)
    age = fields.Date(string="Date Of Birth")
    sex = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female')], default="male")
    address = fields.Text(string="Address")
    phone = fields.Char(string="Phone Number")
    department = fields.Many2one(comodel_name='learn.department', string="Department", domain=[('description', '!=', False), ('description', '!=', '')])
    department_description = fields.Text(string="description by department", related="department.description",
                                         store=True)
    state = fields.Selection(string="state", selection=[('onboard', 'On Board'), ('leave', 'Leave')], default='onboard')
    company_ids = fields.Many2many(comodel_name="learn.company", relation="company_rel", column1="modern_id",
                                   column2="company_id", string="Company")
    dob = fields.Integer(string="age count", compute="get_year_old", store=True)
    reason = fields.Text(string="Reason", readonly=True)
    # active_department = fields.Boolean(string="active department", default=False)

    # @api.onchange("active_department")
    # def _get_active_department(self):
    #     if self.active_department:
    #         return {}
    #     else:
    #         return {'domain': {'department': []}}

    def calculate_age(self, born):
        if born:  # Check if born is a valid date
            today = date.today()
            if born.year > date.today().year:
                return {'warning':
                    {
                        'title': 'warning date calculate',
                        'message': 'Birth date cannot be greater than the current date'
                    }}
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @api.depends('age')
    def get_year_old(self):
        for temp in self:
            if temp.age:
                temp.dob = self.calculate_age(temp.age)
            else:
                temp.dob = 0

    @api.constrains('phone')
    def check_number_phone(self):
        for temp in self:
            if temp.phone and not temp.phone.isdigit():
                raise UserError("phone is not number")

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', False):
            vals_list['name'] = vals_list['name'].title()
        return super(Modern, self).create(vals_list)

    def write(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        return super(Modern,self).write(vals)

    def unlink(self):
        if Modern.phone and Modern.department:
            raise UserError("Modern data is not null")
        return super(Modern, self).unlink()

    def copy(self, default=None):
        default = default or {}
        # default['department'] = 6
        department = self.env['learn.department'].search([('description', '!=', False), ('description', '!=', '')])
        default['department'] = department.id
        return super(Modern, self).copy(default)
    def To_leave(self):
        self.state ='leave'