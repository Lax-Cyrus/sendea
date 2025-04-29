from odoo import models, fields

class Region(models.Model):
    _name = 'sendea.region'
    _description = 'Region'

    name = fields.Char(required=True)
    district_ids = fields.One2many('sendea.district', 'region_id', string='Districts')

class District(models.Model):
    _name = 'sendea.district'
    _description = 'District'

    name = fields.Char(required=True)
    sub_county_ids = fields.One2many('sendea.subcounty', 'district_id', string='Sub-County')
    region_id = fields.Many2one('sendea.region', required=True)

class SubCounty(models.Model):
    _name = 'sendea.subcounty'
    _description = 'Subcounty'

    name = fields.Char(required=True)
    district_id = fields.Many2one('sendea.district', required=True)
    parish_ids = fields.One2many('sendea.parish', 'sub_county_id', string='Parishes')

class Parish(models.Model):
    _name = 'sendea.parish'
    _description = 'Parish'

    name = fields.Char(required=True)
    sub_county_id = fields.Many2one('sendea.subcounty', required=True)
    village_ids = fields.One2many('sendea.village', 'parish_id', string='Villages')

class Village(models.Model):
    _name = 'sendea.village'
    _description = 'Village'

    name = fields.Char(required=True)
    parish_id = fields.Many2one('sendea.parish', required=True)
