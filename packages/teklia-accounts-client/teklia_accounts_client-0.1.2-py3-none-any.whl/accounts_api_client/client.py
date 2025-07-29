import base64
import binascii
import json
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from nacl.exceptions import BadSignatureError
from nacl.exceptions import ValueError as MessageValueError
from nacl.signing import VerifyKey
from requests.exceptions import HTTPError, JSONDecodeError
from requests.models import Response


class AccountsException(Exception):
    """Base exception from the accounts API client"""

    def __init__(self, detail: str, *args):
        self.detail = detail
        super().__init__(detail, *args)


class ResponseException(AccountsException):
    def __init__(self, response: Response):
        """Get a readable message from Accounts' response"""
        try:
            resp_json = response.json()
        except JSONDecodeError:
            try:
                detail = response.content.decode()
            except UnicodeDecodeError:
                detail = "Unexpected response"
        else:
            if "detail" in resp_json:
                detail = resp_json["detail"]
            else:
                detail = ", ".join(
                    f"{key}: {value}" for key, value in resp_json.items()
                )
        self.status_code = response.status_code
        return super().__init__(detail, response)


class InvalidSignature(AccountsException):
    """The signature could not be verified"""


class LicenseNotFound(ResponseException):
    """HTTP 401 (or HTTP 404), when the license does not exist"""


class LicenseExpired(ResponseException):
    """HTTP 402, when the license is expired or has no credit left"""


class LicenseInvalid(ResponseException):
    """HTTP 403 error, when the license is invalid for the targeted product"""


class ServerError(ResponseException):
    """HTTP 500 error returned from accounts"""


@dataclass
class License:
    class Status(Enum):
        Active = "ACTIVE"
        Inactive = "INACTIVE"
        Expiring = "EXPIRING"
        Expired = "EXPIRED"
        Suspended = "SUSPENDED"
        Banned = "BANNED"

    name: str
    status: Status
    uses: int | None
    max_uses: int | None

    def __post_init__(self):
        self.status = License.Status(self.status)


class AccountsClient:
    _header_signature = "Teklia-Signature"
    _header_keys = ["date", "digest", "host", "request-target"]

    def __init__(
        self, *, base_url: str = "https://accounts.teklia.com", verify_key: str
    ) -> None:
        self.base_url = base_url
        try:
            self.verify_key = VerifyKey(base64.b64decode(verify_key))
        except (TypeError, ValueError) as e:
            raise Exception(f"Invalid public verification key: {e}.") from e

    def raise_for_response(self, response: Response) -> None:
        if response.status_code in (401, 404):
            raise LicenseNotFound(response)
        elif response.status_code == 402:
            raise LicenseExpired(response)
        elif response.status_code == 403:
            raise LicenseInvalid(response)
        elif 500 <= response.status_code < 600:
            raise ServerError(response)
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise AccountsException("Unexpected error from accounts") from e

    def get_license(self, license_key: str) -> License:
        """Retrieve details about a license from its key"""
        response = self.request(
            path="/api/v1/license/",
            headers={"Authorization": f"License {license_key}"},
        )
        self.raise_for_response(response)

        try:
            license_attrs = response.json()
        except JSONDecodeError as e:
            raise AccountsException(
                "Accounts did not return a valid JSON response"
            ) from e
        try:
            return License(**response.json())
        except (TypeError, ValueError) as e:
            raise AccountsException(
                f"License has unknown status: {license_attrs['status']}"
            ) from e

    def publish_action(
        self, license_key: str, product_slug: str, action_slug: str
    ) -> None:
        """Perform an action on a product"""
        response = self.request(
            method="post",
            path=f"/api/v1/product/{product_slug}/action/{action_slug}/",
            headers={"Authorization": f"License {license_key}"},
        )
        self.raise_for_response(response)

    def check_signature(self, *, response: Response) -> None:
        """Check the response emanates from a verified accounts instance"""
        headers = response.headers
        # Check required headers are present
        if not (signature := headers.get(self._header_signature)):
            raise InvalidSignature(
                f"{self._header_signature} header is missing from the response"
            )
        if missing_headers := set(self._header_keys).difference(
            key.lower() for key in response.headers
        ):
            raise InvalidSignature(
                f"Some headers are missing from the response: {missing_headers}"
            )
        # Check signature is correctly formatted
        try:
            signature = base64.b64decode(signature)
        except binascii.Error as e:
            raise InvalidSignature(
                f"{self._header_signature} header must be a valid base64 string"
            ) from e
        if len(signature) != 64:
            raise InvalidSignature(
                f"{self._header_signature} signature must be 64 bytes length"
            )
        # Ensure the signature is valid
        payload = {key: headers[key] for key in self._header_keys}
        message = json.dumps(payload, indent=4, sort_keys=True).encode()
        try:
            self.verify_key.verify(message, signature)
        except (MessageValueError, BadSignatureError) as e:
            raise InvalidSignature("Signature could not be verified") from e

    def request(
        self,
        *,
        path: str,
        method: str = "get",
        json: dict | None = None,
        headers: dict | None = None,
    ) -> Response:
        """Generic method to make API requests towards the accounts instance"""
        url = urljoin(self.base_url, path)
        try:
            response = getattr(requests, method)(url, headers=headers)
        except ConnectionError as e:
            # Could be anything else e.g. ConnectionError
            raise AccountsException(
                "Unexpected error retrieving the license from accounts"
            ) from e
        self.check_signature(response=response)
        return response
