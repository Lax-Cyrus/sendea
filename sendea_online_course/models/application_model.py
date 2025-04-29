from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import datetime


level_knowledge = [
        ('zore', 'Not at all'),
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate')
    ]
earning_type = [
        ('month', 'Monthly'),
        ('seasonal', 'Seasonal')
    ]
STATE = [
        ('draft', 'New Application'),        
        ('registered', 'Registered'),
    ]

class Application(models.Model):
    _name = 'sendea.application'
    _description = 'Online Course Application'


    @api.model
    def _get_current_date(self):
        """:return current date """
        return fields.Date.today()
    
    @api.model
    def _get_default_company(self):
        company = self.env.company
        return company

    name = fields.Char(string='Name', required=True)
    user_id = fields.Many2one('res.users', 'User')
    email = fields.Char(string='Email', required=True)
    date_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')
    contact_number = fields.Char(string='Contact Number')
    nin_number = fields.Char(string='NIN Number')
    image_1920 = fields.Binary("", attachment=True, store=True)
    state = fields.Selection(STATE, default='draft')
    company_id = fields.Many2one('res.company', 'Company', default=_get_default_company)
    # Location fields
    region = fields.Many2one('sendea.region', string='Region')
    district = fields.Many2one('sendea.district', string="District")
    sub_county = fields.Many2one('sendea.subcounty', string="Sub County")
    village = fields.Many2one('sendea.village', string="Village")
    parish = fields.Many2one('sendea.parish', string="Parish")   
    nationality = fields.Many2one('res.country', string='Nationality')
    present_address = fields.Char(string="Present Address")
    contact_number = fields.Char(string="Contact No ")
    email = fields.Char(string="Email")
    name_next_kin = fields.Char(string="Name of Next of Kin")
    address_next_kin = fields.Char(string="Address of Next of Kin")
    email_next_kin = fields.Char(string="Email of Next of Kin")
    tel_next_kin = fields.Char(string="Tel.Contact")
    reason_interested_area = fields.Text(string="Reason for For attending PV Solar Systems Training")
    expectation_interested_area = fields.Char(string="Expectation From the Training")
    number_installations = fields.Integer(string="Number of Installations")
    place_installation = fields.Char(string="Place of Installations")
    type_installations = fields.Char(string="Type / Size of Systems installed")
    level_knowledge = fields.Selection(level_knowledge, string="Level of Knowledge in PV Solar Systems Design")
    amount_earned = fields.Text(string="Amount Earned")
    earning_types = fields.Selection(earning_type, string="Earing Type")
    declaration = fields.Text(string="Declaration By the Applicant")
    recommendation_attachment = fields.Binary(string="Recommendation by Employer if Any or LC1 Chairman")
    institute_ids = fields.One2many('institute.record', 'application_id', string="Institutes")
    employment_ids = fields.One2many('employment.record', 'application_id', string="Employment Records")

    def action_register(self):
        """This method moves the state from 'draft' to 'registered'."""
        for record in self:
            if record.state == 'draft':
                record.state = 'registered'
            else:
                raise UserError(_("Only applications in draft state can be registered."))
    
    def _get_customer_information(self):
        """
        This is a placeholder for the required method that the mail template is expecting.
        Return customer-related information or just a default value if needed.
        """
        return {
            'customer_name': self.name,
            'customer_email': self.email,
        }
            
    def send_email_wizard(self):
        self.ensure_one()
        template_id = self.env.ref('sendea_online_course.online_course_application_approved_email', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model="sendea.application",
            default_res_ids=[int(self.id)],  # Ensure it's a list of integers
            default_use_template=bool(template_id),
            default_template_id=template_id.id,
            default_composition_mode='comment',
            default_is_log=False,
            custom_layout='mail.mail_notification_light',
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def application_approval(self):
        self.approval_date = datetime.datetime.now()
        self.write({'state': 'registered'})
        
        # Get the email template
        mail_template = self.env.ref('sendea_online_course.online_course_application_approved_email', raise_if_not_found=False)        
        mail_template.sudo().send_mail(self.id, force_send=True)
            
   
            
    @api.onchange('region')
    def _onchange_region(self):
        self.district = False
        self.sub_county = False
        self.parish = False
        self.village = False
        return {'domain': {'district': [('region_id', '=', self.region.id)]}}

    @api.onchange('district')
    def _onchange_district(self):
        self.sub_county = False
        self.parish = False
        self.village = False
        return {'domain': {'sub_county': [('district_id', '=', self.district.id)]}}

    @api.onchange('sub_county')
    def _onchange_sub_county(self):
        self.parish = False
        self.village = False
        return {'domain': {'parish': [('sub_county_id', '=', self.sub_county.id)]}}

    @api.onchange('parish')
    def _onchange_parish(self):
        self.village = False
        return {'domain': {'village': [('parish_id', '=', self.parish.id)]}}
            

class InstituteRecord(models.Model):
    _name = 'institute.record'
    _description = 'Institute Record for Course Application'

    application_id = fields.Many2one('sendea.application', string="Application", ondelete='cascade')
    name = fields.Char(string="Institute")
    year_training = fields.Char(string="Year")
    qualification = fields.Char(string="Qualification")

class EmploymentRecord(models.Model):
    _name = 'employment.record'
    _description = 'Employment Record for Course Application'

    application_id = fields.Many2one('sendea.application', string="Application", ondelete='cascade')
    employer_name = fields.Char(string="Name of Employer")
    starting_year = fields.Char(string="Starting Year")
    ending_year = fields.Char(string="Ending Year")






