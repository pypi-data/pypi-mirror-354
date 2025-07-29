# Copyright (C) 2020 Terrabit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# Generare note contabile la achizitie
import logging

from odoo.tests import Form, tagged

from odoo.addons.l10n_ro_stock_account.tests.common import TestStockCommon

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install")
class TestStockSale(TestStockCommon):
    def test_sale_notice_and_invoice(self):
        """
        - initial in stoc si contabilitate este valoarea din achizitie
        - dupa vanzare valoarea stocului trebuie sa scada cu valoarea stocului
        vandut
        - valoarea din stoc trebuie sa fie egala cu valoarea din contabilitate
        - in contul de venituri trebuie sa fie inregistrata valoarea de vanzare
        """

        self.make_purchase()

        self.check_stock_valuation(self.val_p1_i, self.val_p2_i)
        self.check_account_valuation(self.val_p1_i, self.val_p2_i)

        self.create_so(vals={"l10n_ro_notice": True})

        # valoarea de stoc dupa vanzarea produselor
        val_stock_p1 = round(self.val_p1_i - self.val_stock_out_so_p1, 2)
        val_stock_p2 = round(self.val_p2_i - self.val_stock_out_so_p2, 2)

        self.check_stock_valuation(val_stock_p1, val_stock_p2)

        # inca nu se face si descaracarea contabila de gestiune!
        self.check_account_valuation(val_stock_p1, val_stock_p2)

        self.create_sale_invoice()

        _logger.info("Verifcare valoare ramas in stoc")
        self.check_stock_valuation(val_stock_p1, val_stock_p2)
        self.check_account_valuation(val_stock_p1, val_stock_p2)

        _logger.info("Verifcare valoare vanduta")
        self.check_account_valuation(
            -self.val_so_p1, -self.val_so_p2, self.account_income
        )

    def test_sale_notice_and_invoice_and_return_extra_location_accounts(self):
        """
        - initial in stoc si contabilitate este valoarea din achizitie
        pe contul din locatie
        - dupa vanzare valoarea stocului trebuie sa scada cu valoarea stocului
        vandut
        - valoarea din stoc trebuie sa fie egala cu valoarea din contabilitate
        - in contul de venituri trebuie sa fie inregistrata valoarea de vanzare
        de pe contul din locatie
        - dupa emiterea facturii contul 418 trebuie sa fie zero
        """
        acc_371 = self.env["account.account"].search([("code", "=", "371000")], limit=1)
        acc_3711 = acc_371.copy(default={"code": "371001"})

        acc_707 = self.env["account.account"].search([("code", "=", "707000")], limit=1)
        acc_7071 = acc_707.copy(default={"code": "707001"})

        acc_607 = self.env["account.account"].search([("code", "=", "607000")], limit=1)
        acc_6071 = acc_607.copy(default={"code": "607001"})

        location_id = (
            self.location_warehouse
            + self.company_data["default_warehouse"].lot_stock_id
        )
        location_id.write(
            {
                "l10n_ro_property_account_income_location_id": acc_7071,
                "l10n_ro_property_account_expense_location_id": acc_6071,
                "l10n_ro_property_stock_valuation_account_id": acc_3711,
            }
        )
        self.make_purchase()

        self.check_stock_valuation(self.val_p1_i, self.val_p2_i, account=acc_3711)
        self.check_account_valuation(self.val_p1_i, self.val_p2_i, account=acc_3711)
        self.create_so(vals={"l10n_ro_notice": True})

        # valoarea de stoc dupa vanzarea produselor
        val_stock_p1 = round(self.val_p1_i - self.val_stock_out_so_p1, 2)
        val_stock_p2 = round(self.val_p2_i - self.val_stock_out_so_p2, 2)

        self.check_stock_valuation(val_stock_p1, val_stock_p2, account=acc_3711)
        self.check_account_valuation(val_stock_p1, val_stock_p2, account=acc_3711)

        _logger.info("Verifcare valoare descarcata")
        self.check_account_valuation(
            self.val_stock_out_so_p1, self.val_stock_out_so_p2, account=acc_6071
        )

        _logger.info("Verifcare valoare vanduta")
        self.check_account_valuation(-self.val_so_p1, -self.val_so_p2, acc_7071)

        _logger.info("Verifcare valoare 418")
        self.check_account_valuation(
            self.val_so_p1,
            self.val_so_p2,
            account=self.stock_picking_receivable_account_id,
        )

        self.create_sale_invoice()

        _logger.info("Verifcare ca s-a inchis 418")
        self.check_account_valuation(
            0.0, 0.0, account=self.stock_picking_receivable_account_id
        )

        self.check_stock_valuation(val_stock_p1, val_stock_p2, account=acc_3711)
        self.check_account_valuation(val_stock_p1, val_stock_p2, account=acc_3711)

        #####RETURN

        pick = self.so.picking_ids
        stock_return_picking_form = Form(
            self.env["stock.return.picking"].with_context(
                active_ids=pick.ids, active_id=pick.ids[0], active_model="stock.picking"
            )
        )
        return_wiz = stock_return_picking_form.save()
        return_wiz.product_return_moves.write(
            {"quantity": 2.0, "to_refund": True}
        )  # Return only 2
        return_pick = return_wiz._create_return()

        # Validate return picking

        for move in return_pick.move_ids:
            move._set_quantity_done(move.product_uom_qty)
        return_pick.l10n_ro_notice = True
        return_pick.button_validate()

        val_stock_p1 = round(
            self.val_p1_i - self.val_stock_out_so_p1 + 2 * self.price_p1, 2
        )
        val_stock_p2 = round(
            self.val_p2_i - self.val_stock_out_so_p2 + 2 * self.price_p2, 2
        )

        self.check_stock_valuation(val_stock_p1, val_stock_p2, account=acc_3711)
        self.check_account_valuation(val_stock_p1, val_stock_p2, account=acc_3711)

        _logger.info("Verifcare valoare vanduta dupa retur")

        val_so_p1 = round((self.qty_so_p1 - 2) * self.list_price_p1, 2)
        val_so_p2 = round((self.qty_so_p2 - 2) * self.list_price_p2, 2)

        self.check_account_valuation(-val_so_p1, -val_so_p2, acc_7071)

        _logger.info("Verifcare valoare 418 dupa retur")
        # 418 a fost pe 0, inainte de retur, cand s-a facut factura)
        # asadar acum ar trebui sa avem in 418 doar valoarea stornata
        # pe credit (sau pe debit cu -)
        val_so_p1_418 = round(2 * self.list_price_p1, 2)
        val_so_p2_418 = round(2 * self.list_price_p2, 2)

        self.check_account_valuation(
            -val_so_p1_418,
            -val_so_p2_418,
            account=self.stock_picking_receivable_account_id,
        )

        self.create_sale_invoice(final=True)

        _logger.info("Verifcare ca s-a inchis 418 dupa crearea facturii storno")
        self.check_account_valuation(
            0.0, 0.0, account=self.stock_picking_receivable_account_id
        )

    def test_sale_notice_and_invoice_and_retur(self):
        """
        Vanzare si facturare
         - initial in stoc si contabilitate este valoarea din achizitie
         - dupa livrare valoarea stocului trebuie sa scada cu valoarea stocului vandut
         - trebuie sa se inregistreze in contul 418 valoare de vanzare
         - valoarea din stoc trebuie sa fie egala cu valoarea din contabilitate
         - in contul de venituri trebuie sa fie inregistrata valoarea de vanzare
         - dupa facturare soldul contului 418 trebuie sa fie zero
        """

        #  intrare in stoc
        self.make_purchase()

        # iesire din stoc prin vanzare
        self.create_so(vals={"l10n_ro_notice": True})
        pick = self.so.picking_ids

        stock_return_picking_form = Form(
            self.env["stock.return.picking"].with_context(
                active_ids=pick.ids, active_id=pick.ids[0], active_model="stock.picking"
            )
        )
        return_wiz = stock_return_picking_form.save()
        return_wiz.product_return_moves.write(
            {"quantity": 2.0, "to_refund": True}
        )  # Return only 2
        return_pick = return_wiz._create_return()

        # Validate picking

        for move in return_pick.move_ids:
            move._set_quantity_done(move.product_uom_qty)
        return_pick.l10n_ro_notice = True
        return_pick.button_validate()

        self.create_sale_invoice()

        _logger.info("Verifcare valoare ramas in stoc")

        val_stock_p1 = round(
            self.val_p1_i - self.val_stock_out_so_p1 + 2 * self.price_p1, 2
        )
        val_stock_p2 = round(
            self.val_p2_i - self.val_stock_out_so_p2 + 2 * self.price_p2, 2
        )

        self.check_stock_valuation(val_stock_p1, val_stock_p2)
        self.check_account_valuation(val_stock_p1, val_stock_p2)

        _logger.info("Verifcare valoare vanduta")

        val_so_p1 = round((self.qty_so_p1 - 2) * self.list_price_p1, 2)
        val_so_p2 = round((self.qty_so_p2 - 2) * self.list_price_p2, 2)

        self.check_account_valuation(-val_so_p1, -val_so_p2, self.account_income)
