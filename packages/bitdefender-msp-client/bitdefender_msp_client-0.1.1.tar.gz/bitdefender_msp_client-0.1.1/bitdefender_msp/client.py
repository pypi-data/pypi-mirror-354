import requests
from typing import Dict, List, Optional, Union, Any
from .exceptions import BitdefenderMSPError


class BitdefenderMSPClient:
    """Client for the Bitdefender MSP API"""
    
    BASE_URL = "https://msp.bitdefender.com"
    
    def __init__(self, api_key: str):
        """Initialize the client with an API key
        
        Args:
            api_key: The API key for authentication
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"ApiKey {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response data as dictionary
            
        Raises:
            BitdefenderMSPError: If the API returns an error
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        
        try:
            data = response.json()
        except ValueError:
            data = {}
        
        if not response.ok:
            error_msg = data.get("message", "Unknown error")
            error_code = data.get("code", 0)
            raise BitdefenderMSPError(error_msg, error_code, response.status_code)
        
        return data
    
    # Subscriber methods
    def list_subscribers(self, page: int = 1, limit: int = 20, **filters) -> Dict[str, Any]:
        """List subscribers with optional filtering
        
        Args:
            page: Page number for pagination
            limit: Number of items per page
            **filters: Optional filters (product_id, state, subscription_state, etc.)
            
        Returns:
            Dictionary containing subscribers, count, and query_hash
        """
        params = {"page": page, "limit": limit, **filters}
        return self._request("GET", "/v1/subscribers", params=params)
    
    def create_subscriber(self, 
                         email: Optional[str] = None, 
                         phone: Optional[str] = None,
                         username: Optional[str] = None,
                         external_subscriber_id: Optional[str] = None,
                         lang: Optional[str] = None) -> Dict[str, Any]:
        """Create a new subscriber
        
        Args:
            email: Subscriber's email address
            phone: Subscriber's phone number
            username: Subscriber's username
            external_subscriber_id: External identifier for the subscriber
            lang: Language code (e.g., en_US)
            
        Returns:
            Dictionary containing subscriber_id and enrol_url
            
        Note:
            At least one of email, phone, username, or external_subscriber_id must be provided
        """
        data = {}
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if username:
            data["username"] = username
        if external_subscriber_id:
            data["external_subscriber_id"] = external_subscriber_id
        if lang:
            data["lang"] = lang
            
        if not data:
            raise ValueError("At least one of email, phone, username, or external_subscriber_id must be provided")
            
        return self._request("POST", "/v1/subscribers", json=data)
    
    def get_subscriber(self, subscriber_id: str) -> Dict[str, Any]:
        """Get information about a specific subscriber
        
        Args:
            subscriber_id: The ID of the subscriber
            
        Returns:
            Dictionary containing subscriber information
        """
        return self._request("GET", f"/v1/subscribers/{subscriber_id}")
    
    def delete_subscriber(self, subscriber_id: str) -> Dict[str, Any]:
        """Delete a subscriber
        
        Args:
            subscriber_id: The ID of the subscriber
            
        Returns:
            Dictionary containing the result of the operation
        """
        return self._request("DELETE", f"/v1/subscribers/{subscriber_id}")
    
    # Subscription methods
    def list_subscriptions(self, subscriber_id: str) -> Dict[str, Any]:
        """List all subscriptions for a subscriber
        
        Args:
            subscriber_id: The ID of the subscriber
            
        Returns:
            Dictionary containing subscriptions information
        """
        return self._request("GET", f"/v1/subscribers/{subscriber_id}/subscriptions")
    
    def add_subscription(self, 
                        subscriber_id: str, 
                        product_id: str,
                        trial: bool = False,
                        external_subscription_id: Optional[str] = None,
                        reservation_id: Optional[str] = None) -> Dict[str, Any]:
        """Add a new subscription to a subscriber
        
        Args:
            subscriber_id: The ID of the subscriber
            product_id: The ID of the product to subscribe to
            trial: Whether this is a trial subscription
            external_subscription_id: External identifier for the subscription
            reservation_id: Reservation ID for the subscription
            
        Returns:
            Dictionary containing the subscription_id
        """
        data = {"product_id": product_id}
        if trial:
            data["trial"] = trial
        if external_subscription_id:
            data["external_subscription_id"] = external_subscription_id
        if reservation_id:
            data["reservation_id"] = reservation_id
            
        return self._request("POST", f"/v1/subscribers/{subscriber_id}/subscriptions", json=data)
    
    def get_subscription(self, subscriber_id: str, subscription_id: str) -> Dict[str, Any]:
        """Get information about a specific subscription
        
        Args:
            subscriber_id: The ID of the subscriber
            subscription_id: The ID of the subscription
            
        Returns:
            Dictionary containing subscription information
        """
        return self._request("GET", f"/v1/subscribers/{subscriber_id}/subscriptions/{subscription_id}")
    
    def suspend_subscriptions(self, subscriber_id: str, suspended: bool = True) -> Dict[str, Any]:
        """Suspend or resume all subscriptions for a subscriber
        
        Args:
            subscriber_id: The ID of the subscriber
            suspended: True to suspend, False to resume
            
        Returns:
            Dictionary containing the result of the operation
        """
        data = {"suspended": suspended}
        return self._request("PATCH", f"/v1/subscribers/{subscriber_id}/subscriptions", json=data)
    
    def delete_subscription(self, subscriber_id: str, subscription_id: str) -> Dict[str, Any]:
        """Delete a subscription
        
        Args:
            subscriber_id: The ID of the subscriber
            subscription_id: The ID of the subscription
            
        Returns:
            Dictionary containing the result of the operation
        """
        return self._request("DELETE", f"/v1/subscribers/{subscriber_id}/subscriptions/{subscription_id}")