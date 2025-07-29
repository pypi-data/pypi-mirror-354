import requests
from .auth import AuthUtils

class UserUtils:
    """Utilities for accessing users data via MS Graph API"""

    @staticmethod
    def get_current_user():
        """
        Get information about the currently authenticated user.
        
        Returns:
            dict: User information or None if error.
        """
        access_token = AuthUtils.login()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        user_url = "https://graph.microsoft.com/v1.0/me"
        
        response = requests.get(user_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error retrieving user info: {response.text}")
            return None


    @staticmethod
    def get_user_by_name(name: str):
        """
        [Windows Only] 
        Search for users by display name.
        
        Args:
            name (str): The name to search for (can be partial match).
        
        Returns:
            list: List of users matching the name or empty list if none found.
        """
        access_token = AuthUtils.getEdgeToken()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Use $filter with startswith or contains for flexible name matching
        # Option 1: Exact match
        # filter_query = f"displayName eq '{name}'"
        
        # Option 2: Starts with (recommended for name searches)
        filter_query = f"startswith(displayName,'{name}')"
        

        # Option 3: Contains (broader search)
        # filter_query = f"contains(displayName,'{name}')"
        
        user_url = f"https://graph.microsoft.com/v1.0/users?$filter={filter_query}"
        print(f"Searching for user with filter: {user_url}", flush=True)
        
        response = requests.get(user_url, headers=headers)
        
        if response.status_code == 200:
            users = response.json().get("value", [])
            return users
        else:
            print(f"Error searching for user: {response.text}",flush=True)
            return []