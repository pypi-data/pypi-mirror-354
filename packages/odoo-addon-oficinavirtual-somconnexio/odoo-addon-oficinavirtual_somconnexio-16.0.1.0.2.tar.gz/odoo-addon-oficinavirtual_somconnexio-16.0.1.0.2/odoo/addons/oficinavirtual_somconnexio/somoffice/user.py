import json
import os
import requests
import logging
from odoo.addons.somconnexio.helpers.vat_normalizer import VATNormalizer

from .errors import SomOfficeUserCreationError, SomOfficeUserChangeEmailError

log = logging.getLogger(__name__)


class SomOfficeUser:
    def __init__(self, ref, email, vat, lang, env=None):
        self.ref = ref
        self.email = email
        self.vat = vat
        self.lang = lang
        self.env = env

    @classmethod
    def get(cls, vat):
        endpoint = "api/admin/user/"

        params = {"vat": vat}

        response = SomOfficeClient().send_request("GET", endpoint, params=params)

        return response.json()

    def create(self):
        endpoint = "api/admin/import_user/"

        data = {
            "customerCode": self.ref,
            "customerEmail": self.email,
            "customerUsername": self.vat,
            "customerLocale": self._customerLocale(),
            "resetPassword": bool(os.getenv("SOMOFFICE_RESET_PASSWORD") == "true"),
        }

        response = SomOfficeClient().send_request("POST", endpoint, data=data)
        if response.status_code != 200:
            raise SomOfficeUserCreationError(self.ref, response.json())

    def change_email(self, email):
        endpoint = "api/admin/change_user_email"

        data = {
            "vat": self.vat,
            "new_email": email,
        }

        response = SomOfficeClient().send_request("POST", endpoint, data=data)
        if response.status_code != 200:
            raise SomOfficeUserChangeEmailError(self.ref, response.text)

    def generate_invoice_token(self, invoice_id):
        expiration_time = self.env["ir.config_parameter"].get_param(
            "oficinavirtual_somconnexio.expiration_time_download_invoice_in_seconds"
        )
        user_vat = VATNormalizer(self.vat).convert_spanish_vat()
        endpoint = "api/token/user/{}/invoice/{}/".format(user_vat, invoice_id)
        params = {"expiration_time": expiration_time}
        response = SomOfficeClient().send_request("GET", endpoint, params=params)
        return response.json()

    def _customerLocale(self):
        return {
            "es_ES": "es",
            "ca_ES": "ca",
        }[self.lang]


class SomOfficeClient:
    def __init__(self):
        self.base_url = os.getenv("SOMOFFICE_URL")
        self.user = os.getenv("SOMOFFICE_USER")
        self.password = os.getenv("SOMOFFICE_PASSWORD")

    def send_request(self, verb, endpoint, data=None, params=None):
        return requests.request(
            verb.upper(),
            "{}{}".format(self.base_url, endpoint),
            auth=(self.user, self.password),
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
            params=params,
        )
