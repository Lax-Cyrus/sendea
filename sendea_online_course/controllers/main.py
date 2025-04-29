from odoo import http
from odoo.http import request
import base64
import json

class OnlineCourseApplications(http.Controller):


    @http.route('/sendea/online-application', type="http", auth="user", website=True)
    def OnlineCourseApplication(self, **kw):
        nationality = request.env['res.country'].sudo().search([])
        region = request.env['sendea.region'].sudo().search([])
        district = request.env['sendea.district'].sudo().search([])
        parish = request.env['sendea.parish'].sudo().search([])
        sub_county = request.env['sendea.subcounty'].sudo().search([])
        village = request.env['sendea.village'].sudo().search([])
        return request.render('sendea_online_course.sendea_online_course_application_form', {
            'nationalities': nationality,
            'region': region,
            'district': district,
            'parish': parish,
            'sub_county': sub_county,
            'village': village,
        })
    
    @http.route('/sendea/submit-application', type="http", auth="user", website=True)
    def ApplicationSuccessPage(self, **kw):     
        application = request.env['sendea.application'].sudo().create({
            'name': kw.get('name'),
            'email': kw.get('email'),
            'nationality': kw.get('nationality'),
            'date_birth': kw.get('date_birth'),
            'region': kw.get('region'),
            'district': kw.get('district'),
            'parish': kw.get('parish'),
            'sub_county': kw.get('sub_county'),
            'village': kw.get('village'),
            'contact_number': kw.get('contact_number'),
            'name_next_kin': kw.get('name_next_kin'),
            'address_next_kin': kw.get('address_next_kin'),
            'email_next_kin': kw.get('email_next_kin'),
            'tel_next_kin': kw.get('tel_next_kin'),
            'reason_interested_area': kw.get('reason_interested_area'),
            'expectation_interested_area': kw.get('expectation_interested_area'),
            'number_installations': kw.get('number_installations'),
            'place_installation': kw.get('place_installation'),
            'type_installations': kw.get('type_installations'),
            'level_knowledge': kw.get('level_knowledge'),
            'declaration': kw.get('declaration'),
            'amount_earned': kw.get('amount_earned'),
            'gender': kw.get('gender'),
            'earning_types': kw.get('earning_types'),
            'institute_ids': kw.get('institute_ids'),
            'employment_ids': kw.get('employment_ids'),
            'nin_number': kw.get('nin_number'),

        })

         # Retrieve institute data as lists using getlist
        institute_names = request.httprequest.form.getlist('name_institute[]')
        institute_years = request.httprequest.form.getlist('year_training[]')
        institute_qualifications = request.httprequest.form.getlist('qualification[]')

        for name, year, qualification in zip(institute_names, institute_years, institute_qualifications):
            request.env['institute.record'].sudo().create({
                'application_id': application.id,
                'name': name,
                'year_training': year,
                'qualification': qualification,
            })

        # Retrieve employment data as lists using getlist
        employer_names = request.httprequest.form.getlist('employer_name[]')
        starting_years = request.httprequest.form.getlist('starting_year[]')
        ending_years = request.httprequest.form.getlist('ending_year[]')

        for employer, start_year, end_year in zip(employer_names, starting_years, ending_years):
            request.env['employment.record'].sudo().create({
                'application_id': application.id,
                'employer_name': employer,
                'starting_year': start_year,
                'ending_year': end_year,
            })

        image_file = kw.get('image_1920')
        recommendation_attachment_file = kw.get('recommendation_attachment')
        image_base64 = base64.b64encode(image_file.read()) if image_file else False
        recommendation_attachment_base64 = base64.b64encode(recommendation_attachment_file.read()) if recommendation_attachment_file else False
        
        application.image_1920 = image_base64
        application.recommendation_attachment = recommendation_attachment_base64

        return request.render('sendea_online_course.student_thanks', {})


    @http.route('/get_districts/<int:region_id>', type='json', auth='public')
    def get_districts(self, region_id):
        districts = request.env['sendea.district'].search([('region_id', '=', region_id)])
        return [{'id': district.id, 'name': district.name} for district in districts]

    @http.route('/get_subcounties/<int:district_id>', type='json', auth='public')
    def get_subcounties(self, district_id):
        sub_counties = request.env['sendea.subcounty'].search([('district_id', '=', district_id)])
        return [{'id': sub_county.id, 'name': sub_county.name} for sub_county in sub_counties]

    @http.route('/get_parishes/<int:subcounty_id>', type='json', auth='public')
    def get_parishes(self, subcounty_id):
        parishes = request.env['sendea.parish'].search([('sub_county_id', '=', subcounty_id)])
        return [{'id': parish.id, 'name': parish.name} for parish in parishes]

    @http.route('/get_villages/<int:parish_id>', type='json', auth='public')
    def get_villages(self, parish_id):
        villages = request.env['sendea.village'].search([('parish_id', '=', parish_id)])
        return [{'id': village.id, 'name': village.name} for village in villages]  