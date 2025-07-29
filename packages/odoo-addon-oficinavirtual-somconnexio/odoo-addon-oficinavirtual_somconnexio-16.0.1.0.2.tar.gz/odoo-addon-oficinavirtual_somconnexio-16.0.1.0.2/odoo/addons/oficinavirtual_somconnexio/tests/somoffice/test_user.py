import os
import json
from mock import patch, Mock

from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase
from ...somoffice.user import SomOfficeUser


@patch.dict(
    os.environ,
    {
        "SOMOFFICE_URL": "https://somoffice.coopdevs.org/",
        "SOMOFFICE_USER": "user",
        "SOMOFFICE_PASSWORD": "password",
    },
)
@patch(
    "odoo.addons.oficinavirtual_somconnexio.somoffice.user.requests", spec=["request"]
)  # noqa
class SomOfficeUserTestCase(SCTestCase):
    def test_create(self, mock_requests):
        mock_requests.request.return_value = Mock(spec=["status_code", "json"])
        mock_requests.request.return_value.status_code = 200

        SomOfficeUser(123, "something321@example.com", "1234G", "ca_ES").create()
        mock_requests.request.assert_called_with(
            "POST",
            "https://somoffice.coopdevs.org/api/admin/import_user/",
            headers={"Content-Type": "application/json"},
            auth=("user", "password"),
            data=json.dumps(
                {
                    "customerCode": 123,
                    "customerEmail": "something321@example.com",
                    "customerUsername": "1234G",
                    "customerLocale": "ca",
                    "resetPassword": False,
                }
            ),
            params=None,
        )

    def test_create_with_locale_es(self, mock_requests):
        mock_requests.request.return_value = Mock(spec=["status_code", "json"])
        mock_requests.request.return_value.status_code = 200

        SomOfficeUser(123, "something321@example.com", "1234G", "es_ES").create()
        mock_requests.request.assert_called_with(
            "POST",
            "https://somoffice.coopdevs.org/api/admin/import_user/",
            headers={"Content-Type": "application/json"},
            auth=("user", "password"),
            data=json.dumps(
                {
                    "customerCode": 123,
                    "customerEmail": "something321@example.com",
                    "customerUsername": "1234G",
                    "customerLocale": "es",
                    "resetPassword": False,
                }
            ),
            params=None,
        )

    @patch.dict(os.environ, {"SOMOFFICE_RESET_PASSWORD": "true"})
    def test_create_reset_password(self, mock_requests):
        mock_requests.request.return_value = Mock(spec=["status_code", "json"])
        mock_requests.request.return_value.status_code = 200

        SomOfficeUser(123, "something321@example.com", "1234G", "es_ES").create()
        mock_requests.request.assert_called_with(
            "POST",
            "https://somoffice.coopdevs.org/api/admin/import_user/",
            headers={"Content-Type": "application/json"},
            auth=("user", "password"),
            data=json.dumps(
                {
                    "customerCode": 123,
                    "customerEmail": "something321@example.com",
                    "customerUsername": "1234G",
                    "customerLocale": "es",
                    "resetPassword": True,
                }
            ),
            params=None,
        )

    @patch.dict(os.environ, {"SOMOFFICE_RESET_PASSWORD": "true"})
    def test_create_reset_password(self, mock_requests):
        with self.assertRaises(KeyError):
            SomOfficeUser(123, "something321@example.com", "1234G", "en_EN").create()

    def test_get(self, mock_requests):
        vat = "ES123456A"
        expected_somoffice_user_info = {
            "vat": vat,
            "email": "test@test.com",
            "lang": "es_ES",
        }

        def _side_effect_request(verb, endpoint, auth, data, headers, params):
            if (
                verb == "GET"
                and endpoint == "https://somoffice.coopdevs.org/api/admin/user/"
                and auth == ("user", "password")
                and data == "null"
                and headers == {"Content-Type": "application/json"}
                and params == {"vat": vat}
            ):
                return mock_response

        mock_response = Mock(spec=["json"])
        mock_response.json.return_value = expected_somoffice_user_info
        mock_requests.request.side_effect = _side_effect_request

        somoffice_user_info = SomOfficeUser.get(vat)

        mock_response.json.assert_called_with()
        self.assertEqual(somoffice_user_info, expected_somoffice_user_info)

    def test_change_email(self, mock_requests):
        mock_requests.request.return_value = Mock(spec=["status_code", "text"])
        mock_requests.request.return_value.status_code = 200

        SomOfficeUser(123, "", "1234G", "").change_email("new_email@test.coop")
        mock_requests.request.assert_called_with(
            "POST",
            "https://somoffice.coopdevs.org/api/admin/change_user_email",
            headers={"Content-Type": "application/json"},
            auth=("user", "password"),
            data=json.dumps(
                {
                    "vat": "1234G",
                    "new_email": "new_email@test.coop",
                }
            ),
            params=None,
        )

    def test_generate_invoice_token(self, mock_requests):
        expected_invoice_token = {"invoice_token": "token"}

        def _side_effect_request(verb, endpoint, auth, data, headers, params):
            if (
                verb == "GET"
                and endpoint
                == "https://somoffice.coopdevs.org/api/token/user/ES1234G/invoice/321/"
                and auth == ("user", "password")
                and data == "null"
                and params
                == {
                    "expiration_time": self.env["ir.config_parameter"].get_param(
                        "oficinavirtual_somconnexio.expiration_time_download_invoice_in_seconds" # noqa
                    )
                }
                and headers == {"Content-Type": "application/json"}
            ):
                return mock_response

        mock_response = Mock(spec=["json"])
        mock_response.json.return_value = expected_invoice_token
        mock_requests.request.side_effect = _side_effect_request

        invoice_token = SomOfficeUser(
            "", "", "1234g", "", self.env
        ).generate_invoice_token(321)

        mock_response.json.assert_called_with()
        self.assertEqual(invoice_token, expected_invoice_token)
