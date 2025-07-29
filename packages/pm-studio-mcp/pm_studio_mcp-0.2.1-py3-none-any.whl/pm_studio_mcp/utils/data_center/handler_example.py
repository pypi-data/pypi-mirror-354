from base_handler import BaseHandler
from typing import Dict, Any

class HandlerExample(BaseHandler):
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(HandlerExample, cls).__new__(cls)
        return cls._instance
    
    # Step 1: Initialize your client with necessary parameters
    def __init__(self, client_id: str, client_secret:str):
        # Initialize any necessary resources here
        if self._initialized:
            return
        # self.client = initialize_client(client_id, client_secret)
        pass

    # Step 2: Implement the method to fetch data using the client
    def fetch_data(self, query: str, working_dir: str = "") -> Dict[str, Any]:
        """
        Fetch data based on the provided query.
        
        :param query: The query string to search for.
        :return: Example data fetched based on the query.
        """
        # Implement the logic to fetch data based on the query
        print(f"Fetching data for query '{query}' with parameter '{self.example_param}'.")

        # Write output into a file under working_dir if needed

        # Return the path to your file
        return {"query": query, "example_param": self.example_param, "data": []}
    

# Step 3: Test your functionality
if __name__ == "__main__":
    # put your test code here
    handler = HandlerExample(client_id="your_client_id", client_secret="your_client_secret")
    result = handler.fetch_data(query="example_query")
    print(result)  # This should print the fetched data based on the query