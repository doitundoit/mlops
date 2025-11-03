###  Create a Vertex AI Search app.

# Navigate to AI Applications by searching for it at the top of the console.
# From the left-hand navigation menu, select Data Stores.
# Select Create Data Store.
# Find the Cloud Storage card and click Select on it.
# Select Unstructured documents (PDF, HTML, TXT and more)
# For a GCS path, enter qwiklabs-gcp-02-ed71a212b9cb-bucket/planet-search-docs.
# Keep the location set to global.
# For a data store name, enter: Planet Search

# Click Apps on the left-hand nav.
# Click Create a new app.
# Find the card for a Custom search (general) app and click Create.
# Name the app Planet Search
# Provide a Company name of Planet Conferences
# Select the checkbox next to the Planet Search data store.
# Copy the ID value of your app displayed in the Apps table. Save it in a text document as you will need it later.

import os
import sys
sys.path.append("..")
import google.cloud.logging
from callback_logging import log_query_to_model, log_model_response
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools import AgentTool

from .tools import get_date

# Add the VertexAiSearchTool import below
from google.adk.tools import VertexAiSearchTool

load_dotenv()
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

# Create your vertexai_search_tool and update its path below
PROJECT_ID = "qwiklabs-gcp-02-ed71a212b9cb"
SEARCH_APP_ID = "planet-search_1761529350352"
vertexai_search_tool = VertexAiSearchTool(
    search_engine_id=f"projects/{PROJECT_ID}/locations/global/collections/default_collection/engines/{SEARCH_APP_ID}"
)

# wrap an agent with a search tool with an AgentTool
vertexai_search_agent = Agent(
    name="vertexai_search_agent",
    model=os.getenv("MODEL"),
    instruction="Use your search tool to look up facts.",
    tools=[vertexai_search_tool]
)

root_agent = Agent(
    # A unique name for the agent.
    name="root_agent",
    # The Large Language Model (LLM) that agent will use.
    model=os.getenv("MODEL"),
    # A short description of the agent's purpose, so other agents
    # in a multi-agent system know when to call it.
    description="Answer questions using your data store access.",
    # Instructions to set the agent's behavior.
    instruction="You analyze new planet discoveries and engage with the scientific community on them.",
    # Callbacks to log the request to the agent and its response.
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    # Add the tools instructed below
    # tools=[vertexai_search_tool]
    tools=[
        # agent-as-a-tool
        AgentTool(vertexai_search_agent, skip_summarization=False),
        get_date
    ] 
)
