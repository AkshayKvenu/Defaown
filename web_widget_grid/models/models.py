# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import UserError

class RiskCriteria(models.Model):
    _name = 'risk.criteria'
    
    relation_id = fields.Many2one('mrp.production', string="Reverse relation")
    name = fields.Char(string="Name")
    color = fields.Char(string="color")
    score_min = fields.Integer(string="Score Min")
    score_max = fields.Integer(string="Score Max")
    


class MRP(models.Model):
    _inherit = 'mrp.production'
    
    html_view = fields.Html('HTML View',compute="_create_html_view")
    risk_criteria_ids = fields.One2many('risk.criteria', 'relation_id', string="Risk Criterias")
            
    @api.depends('risk_criteria_ids','risk_criteria_ids.color')
    def _create_html_view(self):
        likelihood = 7
        impact = 5
        col_likelihood = [i for i in range(1,likelihood+1)]
        row_impact = [i for i in range(1,impact+1)]
        row_impact.reverse()
        
        tbody = ''
        for line in row_impact:
            row = ''
            for item in col_likelihood:
                cell_val = line+item
                color_pick = 'black'
                for criteria in self.risk_criteria_ids:
                    if criteria.score_min <= cell_val <= criteria.score_max:
                        color_pick = criteria.color
                row += '<td style="border-right:1px solid black;background-color:%s;text-align:center;width:50px;height:50px">%s</td>' % (color_pick, cell_val)
            tbody += '<tr style="border-bottom:1px solid black">%s</tr>' % row
        tbody = '<tbody>%s</tbody>' % tbody
        self.html_view = '<div class="col-xs-12"><div class="col-xs-1"><strong>Impact</strong></div><div class="col-xs-10"><table style="border:1px solid black">%s</table></div></div><div class="col-xs-2 col-xs-offset-1" style="margin-top:10px;margin-bottom:10px"><strong style="padding-left:17px">Likelihood</strong></div>' % (tbody)
        

