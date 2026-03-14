from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools import VertexAiSearchTool

flooring_chat_agent_vertex_ai_search_agent = LlmAgent(
  name='Flooring_chat_agent_vertex_ai_search_agent',
  model='gemini-2.5-flash',
  description=(
      'Agent specialized in performing Vertex AI Search.'
  ),
  sub_agents=[],
  instruction='Use the VertexAISearchTool to find information using Vertex AI Search.',
  tools=[
    VertexAiSearchTool(
      data_store_id='projects//locations/global/collections//dataStores/'
    )
  ],
)
root_agent = LlmAgent(
  name='Flooring_chat_agent',
  model='gemini-2.5-flash',
  description=(
      'To chat with customers'
  ),
  sub_agents=[],
  instruction='You are a chat agent and your name is Aphia who will welcome customers on behalf of AfterFiveFloors, a flooring company. You can use this website to get the information about this company and the services they offer - https://www.afterfivefloors.com. You will gather the customer name, email address and their house address and ask if you can book their appointment. Ask them for phone number. \nUse this link to book my appointment in my google calendar https://calendar.app.google/2LqDX4nWkV6Ve1UE6\nShow first 3 1 hour slots for appointment to customer. let them select one. ',
  tools=[

  ],
)