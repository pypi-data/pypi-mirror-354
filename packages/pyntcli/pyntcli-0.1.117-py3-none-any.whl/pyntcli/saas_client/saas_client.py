import os
import requests

import pyntcli.log.log as log
from pyntcli.store import CredStore

PYNT_SAAS = os.environ.get("PYNT_SAAS_URL", "https://api.pynt.io/v1")
logger = log.get_logger()

class PyntClient:
    def __init__(self, base_url=PYNT_SAAS):
        self.base_url = base_url

    def _get_headers(self):
        headers = {}
        with CredStore() as store:
            access_token = store.get_access_token()
            token_type = store.get_token_type()
            headers["Authorization"] = f"{token_type} {access_token}"
        return headers

    def get_config(self):
        url = f"{self.base_url}/config"
        headers = self._get_headers()

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()  # returning actual data

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error accessing '{url}': {e}")
            raise e
        except requests.exceptions.RequestException as e:
            logger.error(f"Error accessing '{url}': {e}")

        return None

    def get_application_by_name(self, application_name):
        url = f"{self.base_url}/application/{application_name}"
        headers = self._get_headers()

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()  # returning actual data

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error accessing '{url}': {e}")
            raise e
        except requests.exceptions.RequestException as e:
            logger.error(f"Error accessing '{url}': {e}")

        return None

pynt_client = PyntClient()