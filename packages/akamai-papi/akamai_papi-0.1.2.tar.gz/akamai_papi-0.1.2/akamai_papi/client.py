import requests
from .utils import load_edgerc
from .exceptions import AkamaiPapiError
from akamai.edgegrid import EdgeGridAuth

class PapiClient:
    def __init__(self, edgerc_path="~/.edgerc", section="default"):
        creds = load_edgerc(edgerc_path, section)
        self.base_url = f"https://{creds['host']}"
        self.session = requests.Session()
        self.session.auth = EdgeGridAuth(
            client_token=creds["client_token"],
            client_secret=creds["client_secret"],
            access_token=creds["access_token"]
        )

    def _get(self, endpoint, params=None):
        url = self.base_url + endpoint
        resp = self.session.get(url, params=params)
        if not resp.ok:
            raise AkamaiPapiError(f"GET {url} failed: {resp.status_code} {resp.text}")
        return resp.json()

    def list_groups(self):
        result = self._get("/papi/v1/groups")
        return result.get("groups", {}).get("items", [])

    def list_properties(self, group_id):
        result = self._get("/papi/v1/properties", params={"groupId": group_id})
        return result.get("properties", {}).get("items", [])

    def get_property_rules(self, property_id, version, group_id):
        endpoint = f"/papi/v1/properties/{property_id}/versions/{version}/rules"
        return self._get(endpoint, params={"groupId": group_id})

    def list_contracts(self):
        result = self._get("/papi/v1/contracts")
        return result.get("contracts", {}).get("items", [])

    def get_property_versions(self, property_id, group_id):
        result = self._get(f"/papi/v1/properties/{property_id}/versions", params={"groupId": group_id})
        return result.get("versions", {}).get("items", [])