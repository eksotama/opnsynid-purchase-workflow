# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseOrderType(models.Model):
    _inherit = "purchase.order.type"

    @api.depends(
        "allowed_product_categ_ids",
        "allowed_product_ids",
    )
    def _compute_all_allowed_product_ids(self):
        obj_product = self.env["product.product"]
        for po_type in self:
            products = po_type.allowed_product_ids
            category_ids = po_type.allowed_product_categ_ids.ids
            criteria = [
                ("categ_id", "in", category_ids),
                ("purchase_ok", "=", True),
            ]
            products += obj_product.search(criteria)
            po_type.all_allowed_product_ids = products

    limit_product_selection = fields.Boolean(
        string="Limit Product Selection",
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        relation="product_category_purchase_order_type_rel",
        column1="purchase_order_type_id",
        column2="product_category_id",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Product",
        comodel_name="product.product",
        domain=[("purchase_ok", "=", True)],
        relation="rel_po_type_2_product",
        column1="purchase_order_type_id",
        column2="product_product_id",
    )
    all_allowed_product_ids = fields.Many2many(
        string="All Allowed Product",
        comodel_name="product.product",
        compute="_compute_all_allowed_product_ids",
        store=True,
        relation="rel_po_type_2_all_product",
        column1="purchase_order_type_id",
        column2="product_product_id",
    )
