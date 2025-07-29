# necta_fetcher/client.py (MODIFIED FOR PROXY SUPPORT)
import requests
from bs4 import BeautifulSoup
from .exceptions import (
    NectaLoginError, NectaTokenError, NectaRequestError,
    NectaResultError, NectaStudentNotFoundError
)

class NectaClient:
    """
    A client to fetch NECTA results programmatically via the ajira.zimamoto.go.tz endpoint.
    This version hardcodes login credentials and now supports proxies.
    """
    LOGIN_URL = "https://ajira.zimamoto.go.tz/login"
    TOKEN_UPDATE_URL = "https://ajira.zimamoto.go.tz"
    RESULTS_API_URL = "https://ajira.zimamoto.go.tz/candidates/nectaResult"

    DEFAULT_EMAIL = "adosomeless@gmail.com"
    DEFAULT_PASSWORD = "Someless11"

    # --- KEY CHANGE IS HERE ---
    def __init__(self, email=None, password=None, user_agent=None, timeout=30, proxies=None):
        self.email = email or self.DEFAULT_EMAIL
        self.password = password or self.DEFAULT_PASSWORD
        self.session = requests.Session()
        
        # Configure the session with all settings
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (compatible; NectaFetcherPackage/0.4.1)'
        })
        self.session.timeout = timeout
        if proxies:
            self.session.proxies = proxies
            print("NectaClient session configured with proxies.")
        # --- END OF KEY CHANGE ---

        self._is_logged_in = False
        self._action_csrf_token = None

    def _perform_login(self):
        """Handles the login process."""
        if self._is_logged_in:
            return True

        print("Attempting to log in to NECTA portal (via ajira.zimamoto)...")
        try:
            # All requests now use the pre-configured session (with proxy if set)
            login_page_resp = self.session.get(self.LOGIN_URL)
            login_page_resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise NectaLoginError(f"Error fetching login page: {e}")

        soup = BeautifulSoup(login_page_resp.text, 'html.parser')
        login_token_input = soup.find("input", {"name": "_token"})
        if not login_token_input or not login_token_input.get("value"):
            raise NectaTokenError("Failed to retrieve CSRF token from login page.")
        
        login_csrf_token = login_token_input.get("value")

        login_payload = {
            "email": self.email,
            "password": self.password,
            "_token": login_csrf_token
        }

        try:
            response = self.session.post(self.LOGIN_URL, data=login_payload)
            response.raise_for_status()
            if "dashboard" in response.url.lower() or self.LOGIN_URL not in response.url:
                self._is_logged_in = True
                print("Login successful.")
                if not self._refresh_action_token():
                    self._is_logged_in = False
                    raise NectaTokenError("Login succeeded but failed to refresh action CSRF token.")
                return True
            else:
                soup_fail = BeautifulSoup(response.text, 'html.parser')
                error_div = soup_fail.find('div', class_='alert-danger')
                error_msg = f"Login failed: {error_div.get_text(strip=True)}" if error_div else "Login failed. Credentials may be incorrect or page structure changed."
                raise NectaLoginError(error_msg)
        except requests.exceptions.RequestException as e:
            raise NectaLoginError(f"Login request failed: {e}")

    def _refresh_action_token(self):
        """Refreshes the CSRF token used for POST actions."""
        if not self._is_logged_in:
             raise NectaLoginError("Cannot refresh action token, not logged in.")

        print("Refreshing action CSRF token...")
        try:
            resp = self.session.get(self.TOKEN_UPDATE_URL)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise NectaTokenError(f"Error fetching page to refresh action token: {e}")

        soup = BeautifulSoup(resp.text, 'html.parser')
        token_input = soup.find("input", {"name": "_token"})
        if token_input and token_input.get("value"):
            self._action_csrf_token = token_input.get("value")
            print("Action CSRF token updated.")
            return True
        else:
            meta_tag = soup.find("meta", {"name": "csrf-token"})
            if meta_tag and meta_tag.get("content"):
                self._action_csrf_token = meta_tag.get("content")
                print("Action CSRF token updated from meta tag.")
                return True
            
        self._action_csrf_token = None
        print("Warning: Could not find a new action CSRF token.")
        return False

    def fetch_student_results(self, index_string: str, year: str, exam_level: str):
        """Fetches results for a specific student using the API."""
        if not self._is_logged_in:
            self._perform_login()

        if not self._action_csrf_token:
            print("Action CSRF token missing, attempting refresh...")
            if not self._refresh_action_token() or not self._action_csrf_token:
                raise NectaTokenError("Required action CSRF token is not available.")

        payload = {
            "year": str(year), "number": index_string, "level": exam_level,
            "_token": self._action_csrf_token
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest", "Accept": "application/json, text/javascript, */*; q=0.01",
        }
        
        xsrf_cookie = self.session.cookies.get('XSRF-TOKEN')
        if xsrf_cookie:
            headers["X-XSRF-TOKEN"] = xsrf_cookie

        print(f"Fetching results for {index_string}, Year: {year}, Level: {exam_level}...")
        try:
            response = self.session.post(self.RESULTS_API_URL, data=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                error_details = e.response.json()
                msg = error_details.get("message", str(e))
                if "not found" in msg.lower() or e.response.status_code == 404:
                    raise NectaStudentNotFoundError(f"API Error for {index_string}: {msg} (Status: {e.response.status_code})")
                raise NectaResultError(f"API HTTP Error for {index_string}: {msg} (Status: {e.response.status_code})")
            except ValueError:
                raise NectaRequestError(f"HTTP Error {e.response.status_code} for {index_string}. Response: {e.response.text[:200]}")
        except requests.exceptions.RequestException as e:
            raise NectaRequestError(f"Network or request error for {index_string}: {e}")

        try:
            api_response_json = response.json()
        except ValueError:
            raise NectaResultError(f"Invalid JSON response for {index_string}. Content: {response.text[:500]}")

        if api_response_json.get("success") is True and "data" in api_response_json:
            student_data = api_response_json["data"]
            if isinstance(student_data, dict) and (student_data.get("index_number", "").upper() == index_string.upper() or student_data.get("regno", "").upper() == index_string.upper()):
                if str(student_data.get("first_name", "")).upper() == "N/A" and not student_data.get("subjects"):
                    raise NectaStudentNotFoundError(f"Student {index_string} query returned placeholder 'N/A' data.")
                return student_data
            else:
                raise NectaResultError(f"API success for {index_string}, but 'data' field is not the expected student structure. Data: {str(student_data)[:200]}")
        elif api_response_json.get("success") is False:
            error_message = api_response_json.get("message", "API returned success=false without a message.")
            if "not found" in error_message.lower():
                 raise NectaStudentNotFoundError(f"Student {index_string} not found: {error_message}")
            raise NectaResultError(f"API error for {index_string}: {error_message}")
        else:
            raise NectaResultError(f"Unexpected API response structure for {index_string}. Response: {str(api_response_json)[:500]}")