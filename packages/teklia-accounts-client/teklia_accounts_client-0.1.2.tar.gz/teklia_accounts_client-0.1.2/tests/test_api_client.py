import pytest

from accounts_api_client.client import (
    AccountsClient,
    AccountsException,
    InvalidSignature,
    License,
    LicenseExpired,
    LicenseInvalid,
    LicenseNotFound,
    ServerError,
)


@pytest.mark.parametrize(
    ("status_code", "expected"),
    [
        (401, LicenseNotFound),
        (402, LicenseExpired),
        (403, LicenseInvalid),
        (404, LicenseNotFound),
        (418, AccountsException),
        (501, ServerError),
    ],
)
def test_get_license_error(accounts_mocker, client, status_code, expected):
    accounts_mocker("api/v1/license/", status=status_code)
    with pytest.raises(expected):
        client.get_license(license_key="not_found")


def test_get_license_unexpected_json(accounts_mocker, client):
    accounts_mocker(
        "api/v1/license/",
        json={"status": "AAAA"},
    )
    with pytest.raises(AccountsException):
        client.get_license(license_key="key")


def test_get_license_invalid_signature(accounts_mocker, client):
    accounts_mocker(
        "api/v1/license/",
        json={
            "name": "test",
            "uses": 5,
            "max_uses": 25,
            "status": "ACTIVE",
        },
        headers={"Teklia-Signature": "aaaaaaa"},
    )
    with pytest.raises(InvalidSignature):
        client.get_license(license_key="key")


def test_get_license_invalid_public_key(accounts_mocker):
    accounts_mocker(
        "api/v1/license/",
        json={
            "name": "test",
            "uses": 5,
            "max_uses": 25,
            "status": "ACTIVE",
        },
        headers={"Teklia-Signature": "aaaaaaa"},
    )
    client = AccountsClient(
        base_url="https://accounts.server",
        verify_key="eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg=",
    )
    with pytest.raises(InvalidSignature):
        client.get_license(license_key="key")


def test_get_license(accounts_mocker, client):
    accounts_mocker(
        "api/v1/license/",
        json={
            "name": "test",
            "uses": 5,
            "max_uses": 25,
            "status": "ACTIVE",
        },
    )
    assert client.get_license(license_key="key") == License(
        name="test", status=License.Status.Active, uses=5, max_uses=25
    )


@pytest.mark.parametrize(
    ("status_code", "expected"),
    [
        (401, LicenseNotFound),
        (402, LicenseExpired),
        (403, LicenseInvalid),
        (404, LicenseNotFound),
        (418, AccountsException),
        (501, ServerError),
    ],
)
def test_publish_action_error(accounts_mocker, client, status_code, expected):
    accounts_mocker(
        "api/v1/product/test/action/transcribe/", method="POST", status=status_code
    )
    with pytest.raises(expected):
        client.publish_action(
            license_key="not_found", product_slug="test", action_slug="transcribe"
        )


def test_publish_action_invalid_signature(accounts_mocker, client):
    accounts_mocker(
        "api/v1/product/test/action/transcribe/",
        method="POST",
        headers={"Date": "aaaaaaa"},
    )
    with pytest.raises(InvalidSignature):
        client.publish_action(
            license_key="not_found", product_slug="test", action_slug="transcribe"
        )


def test_publish_action_invalid_public_key(accounts_mocker):
    accounts_mocker("api/v1/product/test/action/transcribe/", method="POST")
    client = AccountsClient(
        base_url="https://accounts.server",
        verify_key="eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg=",
    )
    with pytest.raises(InvalidSignature):
        client.publish_action(
            license_key="not_found", product_slug="test", action_slug="transcribe"
        )


def test_publish_action(accounts_mocker, client):
    accounts_mocker("api/v1/product/test/action/transcribe/", method="POST")
    assert (
        client.publish_action(
            license_key="not_found", product_slug="test", action_slug="transcribe"
        )
        is None
    )
