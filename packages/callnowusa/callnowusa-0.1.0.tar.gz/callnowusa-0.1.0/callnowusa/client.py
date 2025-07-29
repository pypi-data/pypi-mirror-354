import time

import requests
import json
import uuid

class Client:
    """
    Client for interacting with the CallNowUSA

    """
    def __init__(self, account_sid, auth_token, phone_number, base_url="https://callnowusa.onrender.com"):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.phone_number = phone_number
        self.base_url = base_url.rstrip('/')
        self.messages = Messages(self)
        self.calls = Calls(self)

    def _send_request(self, endpoint, payload):
        """
        Send a POST request to the specified endpoint with the given payload.
        Returns the JSON response or raises an exception on failure.
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        try:
            time.sleep(2)
            response = requests.post(url, json=payload, headers=headers, timeout=900)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_msg = response.json().get("error", str(e))
            raise ValueError(f"Request to {endpoint} failed: {error_msg}")
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out after 30 seconds")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request to {endpoint} failed: {str(e)}")

    def messages_create(self, body, from_, to):
        """Send a message via the /send-message endpoint."""
        payload = {
            "account_sid": self.account_sid,
            "auth_token": self.auth_token,
            "phone_number": self.phone_number,
            "body": body,
            "from": from_,
            "to": to
        }
        sid = f"SM_{uuid.uuid4().hex}"
        result = self._send_request("send-message", payload)
        return type('Message', (), {
            'fetch': lambda self: result,
            'sid': sid,
            'client': self
        })()

    def calls_create(self, to, from_, auto_hang=True):
        """Initiate a direct call via the /direct-call endpoint."""
        payload = {
            "account_sid": self.account_sid,
            "auth_token": self.auth_token,
            "phone_number": self.phone_number,
            "from": from_,
            "to": to,
            "auto_hang": auto_hang
        }
        sid = f"CA_{uuid.uuid4().hex}"
        time.sleep(2)

        result = self._send_request("direct-call", payload)
        return type('Call', (), {
            'fetch': lambda self: result,
            'sid': sid,
            'client': self
        })()

    def calls_merge(self, phone_1, phone_2, from_):
        """Initiate a merge call via the /merge-call endpoint."""
        payload = {
            "account_sid": self.account_sid,
            "auth_token": self.auth_token,
            "phone_number": self.phone_number,
            "from": from_,
            "phone_1": phone_1,
            "phone_2": phone_2
        }
        time.sleep(2)

        sid = f"CA_{uuid.uuid4().hex}"
        result = self._send_request("merge-call", payload)
        return type('Call', (), {
            'fetch': lambda self: result,
            'sid': sid,
            'client': self
        })()

    def calls_update(self, sid, status, from_=None, to=None):
        """Update a call's status (e.g., hang up). Note: No dedicated endpoint, simulating via /direct-call."""
        payload = {
            "account_sid": self.account_sid,
            "auth_token": self.auth_token,
            "phone_number": self.phone_number,
            "from": from_ or "",
            "to": to or "",
            "status": status
        }
        result = self._send_request("direct-call", payload)
        return type('Call', (), {
            'fetch': lambda self: result,
            'sid': sid,
            'status': result.get('status', status.lower()),
            'client': self
        })()

class Messages:
    """Namespace for message-related operations."""
    def __init__(self, client):
        self.client = client

    def create(self, body, from_, to):
        """Delegate to Client.messages_create."""
        return self.client.messages_create(body, from_, to)

class Calls:
    """Namespace for call-related operations."""
    def __init__(self, client):
        self.client = client

    def create(self, to, from_, auto_hang=True):
        """Delegate to Client.calls_create."""
        return self.client.calls_create(to, from_, auto_hang)

    def merge(self, phone_1, phone_2, from_):
        """Delegate to Client.calls_merge."""
        return self.client.calls_merge(phone_1, phone_2, from_)

    def __call__(self, sid):
        """Return CallInstance for updating a call."""
        return CallInstance(self.client, sid)

class CallInstance:
    """Helper class for updating a call."""
    def __init__(self, client, sid):
        self.client = client
        self.sid = sid

    def update(self, status, from_=None, to=None):
        """Delegate to Client.calls_update."""
        return self.client.calls_update(self.sid, status, from_, to)