# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class CustomWebsiteSale(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        # Call the super function to retain existing functionality
        super(CustomWebsiteSale, self)._checkout_form_save(mode, checkout, all_values)
        Partner = request.env["res.partner"]

        # Retrieve district_id and ward_id from all_values
        district_id = all_values.get("district_id")
        ward_id = all_values.get("ward_id")

        # Add them to the checkout dictionary if they are provided
        if district_id:
            checkout["district_id"] = int(district_id)
        if ward_id:
            checkout["ward_id"] = int(ward_id)

        # Save the partner with new data
        if mode[0] == "new":
            partner_id = (
                Partner.sudo().with_context(tracking_disable=True).create(checkout).id
            )

        elif mode[0] == "edit":
            partner_id = int(all_values.get("partner_id", 0))
            if partner_id:
                # double check
                order = request.website.sale_get_order()
                shippings = Partner.sudo().search(
                    [("id", "child_of", order.partner_id.commercial_partner_id.ids)]
                )
                if (
                    partner_id not in shippings.mapped("id")
                    and partner_id != order.partner_id.id
                ):
                    return http.Forbidden()
                Partner.browse(partner_id).sudo().write(checkout)
        return partner_id

    def _get_country_related_render_values(self, kw, render_values):
        values = super(CustomWebsiteSale, self)._get_country_related_render_values(
            kw, render_values
        )
        partner_id = kw.get("partner_id")
        mode = kw.get("mode")
        if partner_id and mode == "billing":
            partner = (
                request.env["res.partner"]
                .sudo()
                .search([("id", "=", int(partner_id))], limit=1)
            )
            if partner:
                districts = self.get_districts(partner.state_id.id)
                wards = self.get_wards(partner.district_id.id)
                values.update(
                    {
                        "districts": districts,
                        "selected_district_id": partner.district_id.id,
                        "wards": wards,
                        "selected_ward_id": partner.ward_id.id,
                    }
                )
        return values

    @http.route(
        "/shop/get_districts/<int:state_id>",
        type="json",
        auth="public",
        method=["POST"],
        website=True,
    )
    def get_districts(self, state_id):

        districts = (
            request.env["res.district"].sudo().search([("state_id", "=", state_id)])
        )

        districts_data = [
            {"id": district.id, "name": district.name, "ghn_district_id": district.ghn_district_id} for district in districts
        ]
        return districts_data

    @http.route(
        "/shop/get_wards/<int:district_id>",
        type="json",
        auth="public",
        method=["POST"],
        website=True,
    )
    def get_wards(self, district_id):
        wards = (
            request.env["res.ward"].sudo().search([("district_id", "=", district_id)])
        )
        wards_data = [{"id": ward.id, "name": ward.name} for ward in wards]
        return wards_data
