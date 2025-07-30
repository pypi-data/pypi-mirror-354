class BitdefenderMSPError(Exception):
    """Exception raised for Bitdefender MSP API errors"""
    
    def __init__(self, message: str, error_code: int = 0, status_code: int = 0):
        """Initialize the exception
        
        Args:
            message: Error message
            error_code: API error code
            status_code: HTTP status code
        """
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(f"[{status_code}] {error_code}: {message}")