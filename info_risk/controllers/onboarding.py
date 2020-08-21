# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


class OnboardingController(http.Controller):

    @http.route('/info_risk/info_risk_onboarding_panel', auth='user', type='json')
    def info_risk_onboarding(self):
        """ Returns the `banner` for the sale onboarding panel.
            It can be empty if the user has closed it or if he doesn't have
            the permission to see it. """

        company = request.env.company
        if not request.env.is_admin() or \
           company.sale_quotation_onboarding_state == 'closed':
            return {}

        return {
            'html': request.env.ref('info_risk.info_risk_onboarding_panel').render({
                'company': company,
                'state':  company.get_and_update_sale_quotation_onboarding_state()
            })
        }

    @http.route('/info_risk/info_risk_onboarding_panel_impact', auth='user', type='json')
    def info_risk_onboarding_impact(self):
        """ Returns the `banner` for the sale onboarding panel.
            It can be empty if the user has closed it or if he doesn't have
            the permission to see it. """

        company = request.env.company
        if not request.env.is_admin() or \
           company.onboarding_state_impact == 'closed':
            return {}

        return {
            'html': request.env.ref('info_risk.info_risk_onboarding_panel_impact').render({
                'company': company,
                'state':  company.get_and_update_sale_quotation_onboarding_state()
            })
        }

    @http.route('/info_risk/info_risk_onboarding_panel_scenarios', auth='user', type='json')
    def info_risk_onboarding_scenario(self):
        """ Returns the `banner` for the sale onboarding panel.
            It can be empty if the user has closed it or if he doesn't have
            the permission to see it. """

        company = request.env.company
        if not request.env.is_admin() or \
           company.onboarding_state_scenarios == 'closed':
            return {}

        return {
            'html': request.env.ref('info_risk.info_risk_onboarding_panel_scenarios').render({
                'company': company,
                'state':  company.get_and_update_sale_quotation_onboarding_state()
            })
        }
