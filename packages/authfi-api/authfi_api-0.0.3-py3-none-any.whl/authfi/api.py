# import asyncio
from functools import wraps
import re
from typing import Optional, Union, Any

# import aiohttp
from fido2.utils import websafe_encode
from fido2.webauthn import (
    AttestationConveyancePreference,
    AttestationObject,
    AuthenticatorAttachment,
    AuthenticatorData,
    CollectedClientData,
    PublicKeyCredentialType,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)
from pydantic import field_validator
from pydantic.dataclasses import dataclass
import requests
from requests import Response

@dataclass(eq=True, frozen=True)
class AuthfiApiEntity():
    """
    Represents an authentication entity for the Authfi API.
    
    This class handles validation of API access point URLs and API keys
    to ensure they meet the required format before making API calls.
    
    Attributes:
        accesspoint (str): The API endpoint URL that should match the pattern
                          'https://authfi.authentrend.com/<alphanumeric-with-hyphens>'
        key (str): The API authorization key that should be alphanumeric
    """
    accesspoint: str
    key: str

    @field_validator('accesspoint')
    @classmethod
    def validate_accesspoint(cls, value: str) -> str:
        """Validate accesspoint field"""
        if not isinstance(value, str):
            raise TypeError("accesspoint type should be str")
        pattern = "^(https://authfi.authentrend.com/[a-zA-Z0-9-]+)/*$"
        result = re.match(pattern, value.strip())
        if not result:
            raise ValueError(f"API Accesspoint format is not correct. Should fit '{pattern}'")
        return result.group(1)

    @field_validator('key')
    @classmethod
    def validate_key(cls, value: str) -> str:
        """Validate key field"""
        if not isinstance(value, str):
            raise TypeError("key type should be str")
        pattern = "^[a-zA-Z0-9]+$"
        result = re.match(pattern, value.strip())
        if not result:
            raise ValueError(f"API Key format is not correct. Should fit {pattern}")
        return result.group(0)

class AuthFiApi:
    def __init__(
        self,
        api_accesspoint: str, 
        api_key: str, 
        timeout: int = 10,
        authenticator_attachment: AuthenticatorAttachment = AuthenticatorAttachment.CROSS_PLATFORM,
        require_resident_key: ResidentKeyRequirement = ResidentKeyRequirement.REQUIRED,
        user_verification: UserVerificationRequirement = UserVerificationRequirement.REQUIRED,
        attestation: AttestationConveyancePreference = AttestationConveyancePreference.DIRECT,
    ):
        self._api = AuthfiApiEntity(accesspoint=api_accesspoint, key=api_key)
        self.timeout = timeout
        self.authauthenticator_attachment = authenticator_attachment
        self.require_resident_key = require_resident_key
        self.user_verification = user_verification
        self.attestation = attestation

    @property
    def api(self) -> AuthfiApiEntity:
        """Get api field
        
        Common Usage:
            acc = api.accesspoint
            key = api.key
        """
        return self._api

    @property
    def timeout(self) -> int:
        """Get timeout field"""
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: int) -> int:
        """Validate timeout field"""
        if not isinstance(timeout, int):
            raise TypeError("timeout type should be int")
        elif timeout <= 0:
            raise ValueError("timeout value should larger than 0")
        self._timeout = timeout

    @property
    def headers(self) -> dict:
        """Get Headers, which is used by all API request

        Raises:
            ValueError: If self.api.key is empty or None

        Returns:
            dict: A dict of headers
        """
        if not self.api.key:
            raise ValueError("api_key cannot be empty")
        return {
            "Content-Type": "application/json",
            "AT-X-KEY": self.api.key
        }

    def register_begin(
        self,
        user_name: str,
        user_display_name: Optional[str] = None,
        authenticator_attachment: AuthenticatorAttachment = AuthenticatorAttachment.CROSS_PLATFORM,
        require_resident_key: ResidentKeyRequirement = ResidentKeyRequirement.REQUIRED,
        user_verification: UserVerificationRequirement = UserVerificationRequirement.REQUIRED,
        attestation: AttestationConveyancePreference = AttestationConveyancePreference.DIRECT,
        qrcode_token: Optional[str] = None,
    ) -> Response:
        """Begin user registration process for WebAuthn or mobile authentication.

        Args:
            user_name (str): Unique identifier for the user, usually mail
            user_display_name (Optional[str]): Human-readable name for the user, defaults to user_name if None
            authenticator_attachment (AuthenticatorAttachment): Type of authenticator to use
            require_resident_key (ResidentKeyRequirement): Whether to require resident keys (discoverable credentials)
            user_verification (UserVerificationRequirement): User verification requirement
            attestation (AttestationConveyancePreference): Attestation conveyance preference
            qrcode_token (Optional[str]): Optional token for mobile (non-passkey) authentication

        Returns:
            Response: HTTP response from the API
        """
        endpoint = "mobile" if qrcode_token else "webauthn"
        url = f"{self.api.accesspoint}/api/v1/{endpoint}/registration"
        payload = {
            "params": {
                "token": qrcode_token, # Token used ONLY when do non-passkey register
                "user": {
                    "name": user_name,
                    "displayName": user_display_name or user_name
                },
                "authenticatorSelection": {
                    "authenticatorAttachment": authenticator_attachment.casefold(),
                    # "residentKey": require_resident_key.casefold(), # Dummy choice, not used by AuthFi
                    "requireResidentKey": require_resident_key != ResidentKeyRequirement.DISCOURAGED,
                    "userVerification": user_verification.casefold()
                },
                "attestation": attestation.casefold()
            }
        }
        return requests.post(url=url, headers=self.headers, json=payload, timeout=self.timeout)

    def npk_register_begin(
        self,
        qrcode_token: str,
        user_name: str,
        user_display_name: Optional[str] = None,
        authenticator_attachment: AuthenticatorAttachment = AuthenticatorAttachment.CROSS_PLATFORM,
        require_resident_key: ResidentKeyRequirement = ResidentKeyRequirement.REQUIRED,
        user_verification: UserVerificationRequirement = UserVerificationRequirement.REQUIRED,
        attestation: AttestationConveyancePreference = AttestationConveyancePreference.DIRECT,
    ) -> Response:
        """Begin mobile (non-passkey) registration process (convenience method).

        This is a wrapper around register_begin with qrcode_token parameter.

        Args:
            qrcode_token: Token for non-passkey (mobile) authentication
            user_name (str): Unique identifier for the user, usually mail
            user_display_name (Optional[str]): Human-readable name for the user, defaults to user_name if None
            authenticator_attachment (AuthenticatorAttachment): Type of authenticator to use
            require_resident_key (ResidentKeyRequirement): Whether to require resident keys (discoverable credentials)
            user_verification (UserVerificationRequirement): User verification requirement
            attestation (AttestationConveyancePreference): Attestation conveyance preference

        Returns:
            Response: HTTP response from the API
        """
        return self.register_begin(
            user_name=user_name,
            user_display_name=user_display_name,
            authenticator_attachment=authenticator_attachment,
            require_resident_key=require_resident_key,
            user_verification=user_verification,
            attestation=attestation,
            qrcode_token=qrcode_token,
        )

    def register_complete(
        self,
        credential_id: str,
        attestation_object: AttestationObject,
        client_data_json: CollectedClientData,
        credential_type: PublicKeyCredentialType = PublicKeyCredentialType.PUBLIC_KEY,
        get_authenticator_data: Any = None,
        get_public_key: Any = None,
        get_public_key_algorithm: Any = None,
        get_transports: Any = None,
        get_client_extension_results: Any = None,
        qrcode_token: Optional[str] = None,
    ) ->Response:
        """Complete the registration process.

        Args:
            credential_id (str): ID of the credential
            attestation_object (AttestationObject): Attestation object from the authenticator
            client_data_json (CollectedClientData): Client data collected during registration
            credential_type (PublicKeyCredentialType): Type of credential
            get_authenticator_data (Any): Additional authenticator data. Usually NOT USED
            get_public_key (Any): Public key. Usually NOT USED
            get_public_key_algorithm (Any): Algorithm used for the public key. Usually NOT USED
            get_transports (Any): Transport methods. Usually NOT USED
            get_client_extension_results (Any): Client extension results. Usually NOT USED
            qrcode_token (Optional[str]): Optional token for mobile authentication. Usually NOT USED

        Returns:
            Response: HTTP response from the API
        """
        endpoint = "mobile" if qrcode_token else "webauthn"
        url = f"{self.api.accesspoint}/api/v1/{endpoint}/registration"
        payload = {
            "token": qrcode_token, # Token used ONLY when do non-passkey register
            "fido_register_response": {
                "id": websafe_encode(credential_id),
                "rawId": websafe_encode(credential_id),
                "type": credential_type.casefold(),
                "response": {
                    "attestationObject": websafe_encode(attestation_object),
                    "clientDataJSON": websafe_encode(client_data_json),
                    "getAuthenticatorData": get_authenticator_data or {},
                    "getPublicKey": get_public_key or {},
                    "getPublicKeyAlgorithm": get_public_key_algorithm or {},
                    "getTransports": get_transports or {}
                },
                "getClientExtensionResults": get_client_extension_results or {}
            }
        }
        return requests.put(url=url, headers=self.headers, json=payload, timeout=self.timeout)

    def npk_register_complete(
        self,
        qrcode_token: str,
        credential_id: str,
        attestation_object: AttestationObject,
        client_data_json: CollectedClientData,
        credential_type: PublicKeyCredentialType = PublicKeyCredentialType.PUBLIC_KEY,
        get_authenticator_data: Any = None,
        get_public_key: Any = None,
        get_public_key_algorithm: Any = None,
        get_transports: Any = None,
        get_client_extension_results: Any = None,
    ) ->Response:
        """Complete the non-passkey registration process (convenience method).

        This is a wrapper around register_complete with qrcode_token parameter.

        Args:
            qrcode_token: Token for non-passkey (mobile) authentication
            credential_id (str): ID of the credential
            attestation_object (AttestationObject): Attestation object from the authenticator
            client_data_json (CollectedClientData): Client data collected during registration
            credential_type (PublicKeyCredentialType): Type of credential
            get_authenticator_data (Any): Additional authenticator data. Usually NOT USED
            get_public_key (Any): Public key. Usually NOT USED
            get_public_key_algorithm (Any): Algorithm used for the public key. Usually NOT USED
            get_transports (Any): Transport methods. Usually NOT USED
            get_client_extension_results (Any): Client extension results. Usually NOT USED

        Returns:
            Response: HTTP response from the API
        """
        return self.register_complete(
            credential_id=credential_id,
            attestation_object=attestation_object,
            client_data_json=client_data_json,
            credential_type=credential_type,
            get_authenticator_data=get_authenticator_data,
            get_public_key=get_public_key,
            get_public_key_algorithm=get_public_key_algorithm,
            get_transports=get_transports,
            get_client_extension_results=get_client_extension_results,
            qrcode_token=qrcode_token,
        )

    def login_begin(
        self,
        user_verification: UserVerificationRequirement = UserVerificationRequirement.REQUIRED
    ) -> Response:
        """Begin the login process.

        Args:
            user_verification (UserVerificationRequirement): User verification requirement

        Returns:
            Response: HTTP response from the API
        """
        url = f"{self.api.accesspoint}/api/v1/webauthn/login"
        payload = {
            "params": {
                "userVerification": user_verification.casefold()
            }
        }
        return requests.post(url=url, headers=self.headers, json=payload, timeout=self.timeout)

    def login_complete(
        self,
        credential_id: Union[str, bytes],
        authenticator_data: AuthenticatorData,
        signature: Any,
        user_handle: Any,
        client_data_json: Any,
        credential_type: PublicKeyCredentialType = PublicKeyCredentialType.PUBLIC_KEY,
        get_client_extension_results: Any = None
    ) -> Response:
        """Complete the login process.

        Args:
            credential_id (Union[str, bytes]): ID of the credential
            authenticator_data (AuthenticatorData): Authenticator data
            signature (Any): Signature from the authenticator
            user_handle (Any): User handle
            client_data_json (Any): Client data collected during login
            credential_type (PublicKeyCredentialType): Type of credential
            get_client_extension_results (Any): Client extension results

        Returns:
            Response: HTTP response from the API
        """
        url = f"{self.api.accesspoint}/api/v1/webauthn/login"
        payload = {
            "fido_login_response": {
                "id": websafe_encode(credential_id),
                "rawId": websafe_encode(credential_id),
                "type": credential_type.casefold(),
                "response": {
                    "authenticatorData": websafe_encode(authenticator_data),
                    "signature": websafe_encode(signature),
                    "userHandle": websafe_encode(user_handle),
                    "clientDataJSON": websafe_encode(client_data_json)
                },
                "getClientExtensionResults": get_client_extension_results or {}
            }
        }
        return requests.put(url=url, headers=self.headers, json=payload, timeout=self.timeout)

    def authenticate_begin(
        self,
        user_id: Union[str, bytes],
        user_verification: UserVerificationRequirement = UserVerificationRequirement.REQUIRED,
        qrcode_token: Optional[str] = None,
    ) -> Response:
        """Begin the authentication process.

        Args:
            user_id (Union[str, bytes]): ID of the user to authenticate
            user_verification (UserVerificationRequirement): User verification requirement
            qrcode_token (Optional[str]): Optional token for non-passkey (mobile) authentication

        Returns:
            Response: HTTP response from the API
        """
        endpoint = "mobile" if qrcode_token else "webauthn"
        url = f"{self.api.accesspoint}/api/v1/{endpoint}/verification"
        payload = {
            "token": qrcode_token, # Token used ONLY when do non-passkey register
            "uId": websafe_encode(user_id),
            "params": {
                "userVerification": user_verification.casefold()
            }
        }
        return requests.post(url=url, headers=self.headers, json=payload, timeout=self.timeout)

    def npk_authenticate_begin(
        self,
        qrcode_token: str,
        user_id: Union[str, bytes],
        user_verification: UserVerificationRequirement = UserVerificationRequirement.REQUIRED
    ) -> Response:
        """Begin non-passkey authentication process (convenience method).

        This is a wrapper around authenticate_begin with qrcode_token parameter.

        Args:
            qrcode_token (str): Token for non-passkey (mobile) authentication
            user_id (Union[str, bytes]): ID of the user to authenticate
            user_verification (UserVerificationRequirement): User verification requirement

        Returns:
            Response: HTTP response from the API
        """
        return self.authenticate_begin(
            user_id=user_id,
            user_verification=user_verification,
            qrcode_token=qrcode_token
        )

    def authenticate_complete(
        self,
        credential_id: Union[str, bytes],
        authenticator_data: AuthenticatorData,
        signature: Any,
        user_handle: Any,
        client_data_json: Any,
        credential_type: PublicKeyCredentialType = PublicKeyCredentialType.PUBLIC_KEY,
        get_client_extension_results: Any = None,
        qrcode_token: Optional[str] = None,
    ) -> Response:
        """Complete the authentication process.

        Args:
            credential_id (Union[str, bytes]): ID of the credential
            authenticator_data (AuthenticatorData): Authenticator data
            signature (Any): Signature from the authenticator
            user_handle (Any): User handle
            client_data_json (Any): Client data collected during authentication
            credential_type (PublicKeyCredentialType): Type of credential
            get_client_extension_results (Any): Client extension results
            qrcode_token (Optional[str]): Optional token for non-passkey (mobile) authentication

        Returns:
            Response: HTTP response from the API
        """
        endpoint = "mobile" if qrcode_token else "webauthn"
        url = f"{self.api.accesspoint}/api/v1/{endpoint}/verification"
        payload = {
            "token": qrcode_token, # Token used ONLY when do non-passkey register
            "fido_auth_response": {
                "id": websafe_encode(credential_id),
                "rawId": websafe_encode(credential_id),
                "type": credential_type.casefold(),
                "response": {
                    "authenticatorData": websafe_encode(authenticator_data),
                    "signature": websafe_encode(signature),
                    "userHandle": websafe_encode(user_handle),
                    "clientDataJSON": websafe_encode(client_data_json)
                },
                "getClientExtensionResults": get_client_extension_results or {}
            }
        }
        return requests.put(url=url, headers=self.headers, json=payload, timeout=self.timeout)

    def npk_authenticate_complete(
        self,
        qrcode_token: str,
        credential_id: Union[str, bytes],
        authenticator_data: AuthenticatorData,
        signature: Any,
        user_handle: Any,
        client_data_json: Any,
        credential_type: PublicKeyCredentialType = PublicKeyCredentialType.PUBLIC_KEY,
        get_client_extension_results: Any = None
    ) -> Response:
        """Complete non-passkey authentication process (convenience method).

        This is a wrapper around authenticate_complete with qrcode_credit parameter.

        Args:
            qrcode_token (str): Token for non-passkey (mobile) authentication
            credential_id (Union[str, bytes]): ID of the credential
            authenticator_data (AuthenticatorData): Authenticator data
            signature (Any): Signature from the authenticator
            user_handle (Any): User handle
            client_data_json (Any): Client data collected during authentication
            credential_type (PublicKeyCredentialType): Type of credential
            get_client_extension_results (Any): Client extension results

        Returns:
            Response: HTTP response from the API
        """
        return self.authenticate_complete(
            credential_id=credential_id,
            authenticator_data=authenticator_data,
            signature=signature,
            user_handle=user_handle,
            client_data_json=client_data_json,
            credential_type=credential_type,
            get_client_extension_results=get_client_extension_results,
            qrcode_token=qrcode_token,
        )

    def list_users(self, page: int = 1, size: int = 20) -> Response:
        """List users registered in the system.

        Args:
            page (int): Page number for pagination, starting from 1
            size (int): Number of users per page, between 20 and 100

        Raises:
            TypeError: If page or size is not an integer
            ValueError: If size is not within the allowed range [20, 100]

        Returns:
            Response: HTTP response containing user list
        """
        if not isinstance(page, int):
            raise TypeError("page type should be int")
        elif not isinstance(size, int):
            raise TypeError("size type should be int")
        elif not 20 <= size <= 100:
            raise ValueError("size value should in interval [20, 100]")
        url = f"{self.api.accesspoint}/api/v1/users?{page},{size}"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def set_user_state(self, user_id: Union[str, bytes], state: bool) -> Response:
        """Set user state in authenticator (activate or suspend).

        Args:
            user_id (Union[str, bytes]): ID of the user
            state (bool): User state (True for active, False for suspend)

        Returns:
            Response: HTTP response from the API
        """
        url = f"{self.api.accesspoint}/api/v1/users/{websafe_encode(user_id)}"
        payload = {
            "state": "activate" if state else "suspend"
        }
        return requests.put(url=url, headers=self.headers, json=payload, timeout=self.timeout)

    def delete_user(self, user_id: Union[str, bytes]) -> Response:
        """Delete a user from the system.
        
        Args:
            user_id (Union[str, bytes]): ID of the user to delete

        Returns:
            Response: HTTP response from the API
        """
        if isinstance(user_id, bytes):
            user_id = websafe_encode(user_id)
        url = f"{self.api.accesspoint}/api/v1/users/{user_id}"
        return requests.delete(url=url, headers=self.headers, timeout=self.timeout)

    def list_keys(self, user_id: Union[str, bytes]) -> Response:
        """List all authentication keys registered for a given user.

        Args:
            user_id (Union[str, bytes]): ID of the user

        Returns:
            Response: HTTP response containing the keys
        """
        if isinstance(user_id, bytes):
            user_id = websafe_encode(user_id)
        url = f"{self.api.accesspoint}/api/v1/users/{user_id}/keys"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def set_key_name(self, user_id: Union[str, bytes], credential_id: Union[str, bytes], credential_name: str) -> Response:
        """Set a friendly name for a credential.

        Args:
            user_id (Union[str, bytes]): ID of the user
            credential_id (Union[str, bytes]): ID of the credential
            credential_name (str): Friendly name for the credential

        Raises:
            TypeError: If parameters have incorrect types

        Returns:
            Response: HTTP response from the API
        """
        if not isinstance(user_id, (str, bytes)):
            raise TypeError("user_id should be str or bytes")
        elif not isinstance(credential_id, (str, bytes)):
            raise TypeError("credential_id should be str or bytes")
        elif not isinstance(credential_name, str):
            raise TypeError("credential_name should be str")
        if isinstance(user_id, bytes):
            user_id = websafe_encode(user_id)
        url = f"{self.api.accesspoint}/api/v1/users/{user_id}/keys/{credential_id}"
        payload = {
            "name": credential_name
        }
        return requests.put(url=url, headers=self.headers, json=payload, timeout=self.timeout)

    def delete_key(self, user_id: Union[str, bytes], credential_id: Union[str, bytes]) -> Response:
        """Delete a credential for a user.

        Args:
            user_id (Union[str, bytes]): ID of the user
            credential_id (Union[str, bytes]): ID of the credential to delete

        Raises:
            TypeError: If parameters have incorrect types

        Returns:
            Response: HTTP response from the API
        """
        if not isinstance(user_id, (str, bytes)):
            raise TypeError("user_id should be str or bytes")
        elif not isinstance(credential_id, (str, bytes)):
            raise TypeError("credential_id should be str or bytes")
        if isinstance(user_id, bytes):
            user_id = websafe_encode(user_id)
        url = f"{self.api.accesspoint}/api/v1/users/{user_id}/keys/{credential_id}"
        return requests.delete(url=url, headers=self.headers, timeout=self.timeout)

    def generate_registration_qrcode(
        self,
        user_name: str,
        path: str
    ) -> Response:
        """Generate a QR code for registration using an authenticator app.

        Args:
            user_name (str): Name of the user
            path (str): Path for callback after registration

        Returns:
            Response: HTTP response containing the QR code
        """
        url = f"{self.api.accesspoint}/api/v1/mobile/registration/qrcode"
        payload = {
            "params": {
                "user": user_name,
                "path": path
            }
        }
        return requests.post(url=url, headers=self.headers, json=payload, timeout=self.timeout)

    def get_registration_status(self, qrcode_token: str) -> Response:
        """Get the registration result from an authenticator app.

        Args:
            qrcode_id (str): ID of the QR code used for registration

        Returns:
            Response: HTTP response with registration status
        """
        url = f"{self.api.accesspoint}/api/v1/mobile/registration/result/{qrcode_token}"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def get_registered_username(self, qrcode_token: str) -> Response:
        """Get the username of a recently registered user.

        Args:
            qrcode_id (str): ID of the QR code used for registration

        Returns:
            Response: HTTP response containing the username
        """
        url = f"{self.api.accesspoint}/api/v1/mobile/registration/user/{qrcode_token}"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)

    def generate_verification_qrcode(self, path: str) -> Response:
        """Generate a QR code for verification using an authenticator app.

        Args:
            path (str): Path for callback after verification

        Returns:
            Response: HTTP response containing the QR code
        """
        url = f"{self.api.accesspoint}/api/v1/mobile/verification/qrcode"
        payload = {
            "params": {
                "path": path
            }
        }
        return requests.post(url=url, headers=self.headers, json=payload, timeout=self.timeout)

    def get_verification_status(self, qrcode_token: str) -> Response:
        """Get the verification result from an authenticator app.

        Args:
            qrcode_id (str): ID of the QR code used for verification

        Returns:
            Response: HTTP response with verification status
        """
        url = f"{self.api.accesspoint}/api/v1/mobile/verification/result/{qrcode_token}"
        return requests.get(url=url, headers=self.headers, timeout=self.timeout)
