import requests


class QlikReloader:
    def __init__(self, server_url, app_id, cert_path, key_path, user_id="qlik", user_directory="SKL"):
        self.server_url = server_url.rstrip('/')
        self.app_id = app_id
        self.cert = (cert_path, key_path)
        self.xrfkey = "abcdefghijklmnop"
        self.headers = {
            "x-qlik-xrfkey": self.xrfkey,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Qlik-User": f"UserDirectory={user_directory};UserId={user_id}"
        }

    def reload_app(self):
        url = f"{self.server_url}:4242/qrs/app/{self.app_id}/reload"
        params = {"xrfkey": self.xrfkey}

        response = requests.post(
            url,
            headers=self.headers,
            params=params,
            cert=self.cert,
            verify=False
        )

        return response.status_code, response.text
