"""XDBC Client with correct signature format"""

import json
import base64
from datetime import datetime
import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

from .models import XDBResponse
from .exceptions import XDBCException, AuthenticationError, APIError


class XDBCClient:
    """XDBC API Client with ECDSA signatures
    
    This client creates signatures in the format your server expects:
    - ECDSA with SHA256
    - Server-normalized payload formatting
    - DER signature converted to hex, then Base64 encoded
    """
    
    BASE_URLS = {
        "DEV": "http://0.0.0.0:5000",
        "SB": "https://sandbox-api.xdbc.example.com", 
        "PROD": "https://api.xdbc.example.com"
    }
    
    def __init__(self, api_key: str, private_key: str, env: str = "DEV"):
        """Initialize XDBC Client
        
        Args:
            api_key: Your XDBC API key (must exist in database as ACTIVATED)
            private_key: Your ECDSA private key in PEM format
            env: Environment ('DEV', 'SB', 'PROD')
        """
        if not api_key:
            raise AuthenticationError("API key is required")
        if not private_key:
            raise AuthenticationError("Private key is required")
        if env not in self.BASE_URLS:
            raise ValueError(f"Invalid environment. Must be one of: {list(self.BASE_URLS.keys())}")
            
        self.api_key = api_key
        self.env = env
        self.base_url = self.BASE_URLS[env]
        
        # Process and load private key
        self.private_key_pem = self._process_private_key(private_key)
        self.private_key_obj = self._load_private_key()
        
        # Setup session
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "xdbc-client-python/0.1.0"
        })
    
    def _process_private_key(self, private_key: str) -> str:
        """Process private key - handle both escaped and normal newlines"""
        if "\\n" in private_key:
            processed_key = private_key.replace("\\n", "\n")
        else:
            processed_key = private_key
            
        processed_key = processed_key.strip()
        
        if not processed_key.startswith("-----BEGIN"):
            raise AuthenticationError("Private key must be in PEM format")
            
        return processed_key
    
    def _load_private_key(self):
        """Load the ECDSA private key"""
        try:
            private_key_obj = serialization.load_pem_private_key(
                self.private_key_pem.encode('utf-8'),
                password=None,
                backend=default_backend()
            )
            
            if not isinstance(private_key_obj, ec.EllipticCurvePrivateKey):
                raise AuthenticationError("Private key must be an ECDSA/EC private key")
            
            return private_key_obj
        except Exception as e:
            raise AuthenticationError(f"Failed to load private key: {str(e)}")
    
    def _create_signature(self, data_string: str) -> str:
        """Create signature in the correct format
        
        Server expects:
        1. Payload normalized with separators=(",", ":"), ensure_ascii=False
        2. ECDSA SHA256 signature 
        3. DER signature converted to hex, then Base64 encoded
        """
        try:
            # Normalize payload exactly like server does
            payload_normalized = json.dumps(
                json.loads(data_string), 
                separators=(",", ":"), 
                ensure_ascii=False
            )
            
            # Sign the normalized payload using ECDSA with SHA256
            signature_der = self.private_key_obj.sign(
                payload_normalized.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            
            # Convert DER to hex, then Base64 encode the hex bytes
            signature_hex = signature_der.hex().lower()
            signature_b64 = base64.b64encode(bytes.fromhex(signature_hex)).decode('utf-8')
            
            return signature_b64
            
        except Exception as e:
            raise AuthenticationError(f"Failed to create signature: {str(e)}")
        
    def _make_request(self, endpoint: str, data: dict) -> XDBResponse:
        """Make authenticated request"""
        url = f"{self.base_url}{endpoint}"
        
        # Normalize data_string to match server
        data_string = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        
        # Create signature
        signature = self._create_signature(data_string)
        
        # Set headers
        headers = dict(self.session.headers)
        headers["apiKey"] = self.api_key
        headers["signature"] = signature
        
        try:
            response = self.session.post(url, data=data_string, headers=headers, timeout=10)
            
            if response.status_code == 400:
                error_msg = response.text
                if "Connector is inactive" in error_msg:
                    return XDBResponse(
                        status="Failed",
                        message="API key not found or connector inactive in database",
                        error=True
                    )
                elif "API key is invalid" in error_msg:
                    return XDBResponse(
                        status="Failed", 
                        message="API key invalid or public key not found/expired",
                        error=True
                    )
                else:
                    return XDBResponse(
                        status="Failed",
                        message=f"Bad Request: {error_msg}",
                        error=True
                    )
            elif response.status_code == 403:
                return XDBResponse(
                    status="Failed", 
                    message="Signature verification failed - check signature format",
                    error=True
                )
            elif response.status_code == 500:
                return XDBResponse(
                    status="Failed",
                    message="Server error during signature verification",
                    error=True
                )
            
            response.raise_for_status()
            response_data = response.json()
            
            return XDBResponse(
                status=response_data.get("status", "Success"),
                message=response_data.get("message", "Request successful"),
                data=response_data,
                error=False
            )
        except requests.RequestException as e:
            return XDBResponse(
                status="Failed",
                message=f"Request failed: {str(e)}",
                error=True
            )  
            
    def create_memory(self, user_key: str, content: str, tag: str = "", session_id: str = "", reference_id: str = "") -> XDBResponse:
        """Create a new memory
        
        Args:
            user_key: User identifier
            content: Memory content
            tag: Optional tag for categorization
            session_id: Optional session ID (defaults to current hour)
            reference_id: Optional reference ID
            
        Returns:
            XDBResponse: Response object with status, message, and data
        """
        data = {
            "userKey": user_key,
            "content": content,
            "tag": tag,
            "sessionId": session_id or datetime.now().strftime("%Y%m%d%H")
        }
        
        if reference_id:
            data["referenceId"] = reference_id
            
        return self._make_request("/api/memory/create", data)
    
    def retrieve_memory(self, user_key: str, session_id: str = "", tag: str = "") -> XDBResponse:

        data = {
            "userKey": user_key
        }
        
        if session_id:
            data["sessionId"] = session_id
        if tag:
            data["tag"] = tag
            
        return self._make_request("/api/memory/retrieve", data)
    
    def update_memory(self, memory_id: str, content: str, tag: str = "") -> XDBResponse:
        """Update an existing memory
        
        Args:
            memory_id: Memory ID to update
            content: New content
            tag: Optional new tag
            
        Returns:
            XDBResponse: Response object with status, message, and data
        """
        data = {
            "memoryId": memory_id,
            "content": content
        }
        
        if tag:
            data["tag"] = tag
            
        return self._make_request("/api/memory/update", data)
    
    def delete_memory(self, memory_id: str) -> XDBResponse:
        """Delete a memory
        
        Args:
            memory_id: Memory ID to delete
            
        Returns:
            XDBResponse: Response object with status, message, and data
        """
        data = {
            "memoryId": memory_id
        }
        
        return self._make_request("/api/memory/delete", data)