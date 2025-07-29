import sys
import logging

from uuid import uuid4
from importlib import import_module
from importlib.metadata import version
from packaging.version import Version, parse

from .litellm import LiteLLMProvider

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class LLMTracker:
    """
    A class to track and manage different LLM API calls.
    Provides functionality to override API methods and track their usage.
    """

    # Dictionary defining supported API versions and their trackable methods
    SUPPORTED_APIS = {
        # LiteLLM API configuration
        "litellm": {
            "1.3.1": (
                "openai_chat_completions.completion",  # Method to track in LiteLLM
            )
        },
        # OpenAI API configuration (for future implementation)
        "openai": {
            "1.0.0": (
                "chat.completions.create",  # New API endpoint
            ),
            "0.0.0": (
                "ChatCompletion.create",    # Legacy sync endpoint
                "ChatCompletion.acreate",   # Legacy async endpoint
            ),
        }
    }
    llm_provider = None

    def __init__(self, api_key, client="0001"):
        """
        Initialize the LLM tracker.

        Args:
            api_key (str): The API key for authentication
            client (str): Client identifier for tracking purposes
                         Defaults to "0001"
        """
        self.client = client
        self.trace_id = str(uuid4())
        self.api_key = api_key
        self.tags = {}
        logger.info(f"Default client {self.client}")
        print("****************\nGenerated ID: ", self.trace_id, "\n*********\n\n\n\n")

    def add_tags(self, tags):
        """
        Add tags to the current tracking session.
        If tags with the same keys already exist, they will be updated.
        
        Args:
            tags (dict): A dictionary of tags to add/update
        """
        if not isinstance(tags, dict):
            raise ValueError("tags must be a dictionary")
            
        self.tags.update(tags)
        
        # Update tags in the provider if it exists
        if self.llm_provider:
            self.llm_provider.tags = self.tags
            
        logger.info(f"Updated tags: {self.tags}")

    def override_api(self):
        """
        Overrides key methods of the specified API to record events.
        
        This method:
        1. Checks if supported APIs are imported
        2. Verifies version compatibility
        3. Applies appropriate provider patches
        
        Currently only implements LiteLLM support.
        """
        # Iterate through all supported APIs
        for api in self.SUPPORTED_APIS:
            # Check if the API module is imported in the current session
            if api in sys.modules:
                # Import the module dynamically
                module = import_module(api)
                
                # Handle LiteLLM specifically
                if api == "litellm":
                    try:
                        # Get the installed version of LiteLLM
                        module_version = version(api)
                    except Exception as e:
                        logger.warning(f"Cannot determine LiteLLM version: {e}. Only LiteLLM>=1.3.1 supported.")
                        return
                    
                    # Version compatibility check
                    if Version(module_version) >= parse("1.3.1"):
                        logger.info(f"LiteLLM version {module_version} detected. Applying patches...")
                        # Initialize and apply LiteLLM provider patches
                        if not self.llm_provider:
                            self.llm_provider = LiteLLMProvider(
                                trace_id=self.trace_id, 
                                client=self.client, 
                                api_key=self.api_key,
                                tags=self.tags
                            )  # The class from .litellm file
                            self.llm_provider.override()  # Apply override
                        logger.info("LiteLLM override applied successfully.")
                    else:
                        logger.warning(f"Only LiteLLM>=1.3.1 supported. Found v{module_version}. Skipping patch.")
                    
                    # Exit after patching LiteLLM (no need to patch underlying APIs)
                    return

        # Log warning if no supported API modules were found
        logger.warning("No supported LLM module found. Only LiteLLM>=1.3.1 is supported.")

    def stop_instrumenting(self):
        """
        Stops tracking by removing all API patches.
        Currently only removes LiteLLM patches.
        """
        logger.info("Reverting LiteLLM patches...")
        self.llm_provider.undo_override()
        logger.info("LiteLLM patches reverted successfully.")