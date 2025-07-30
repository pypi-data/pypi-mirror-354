from urllib.parse import urljoin
import requests
from .APIRepo import APIRepo

class ReportsRepo(APIRepo):
    """
    ReportsRepo is responsible for generating reports by making API requests to a specified endpoint.
    """
    
    def generate(self, body: dict):
        """
        Generates a report by making a POST request to the 'reports/generate' endpoint.

        Parameters:
        body (dict): The payload to be sent in the POST request.

        Returns:
        requests.Response: The response object resulting from the POST request.

        Raises:
        requests.exceptions.RequestException: An error occurred during the request.
        """
        endpoint = urljoin(self.url, "reports/generate")
        try:
            response = requests.post(endpoint, json=body, stream=True)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            return response
        except requests.exceptions.RequestException as e:
            # Handle the error, log it, or re-raise it
            print(f"An error occurred: {e}")
            raise
