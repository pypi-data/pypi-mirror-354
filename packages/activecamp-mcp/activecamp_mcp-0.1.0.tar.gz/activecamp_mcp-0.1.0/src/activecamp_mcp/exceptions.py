"""Custom exceptions for ActiveCampaign MCP server."""


class ActiveCampaignMCPError(Exception):
    """Base exception for ActiveCampaign MCP server."""
    pass


class APIError(ActiveCampaignMCPError):
    """Error communicating with ActiveCampaign API."""

    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class AutomationNotFoundError(ActiveCampaignMCPError):
    """Automation not found error."""

    def __init__(self, automation_id: str):
        super().__init__(f"Automation {automation_id} not found")
        self.automation_id = automation_id


class CacheError(ActiveCampaignMCPError):
    """Error with cache operations."""
    pass


class AnalysisError(ActiveCampaignMCPError):
    """Error during automation analysis."""

    def __init__(self, message: str, automation_id: str = None):
        super().__init__(message)
        self.automation_id = automation_id


class ValidationError(ActiveCampaignMCPError):
    """Data validation error."""
    pass

