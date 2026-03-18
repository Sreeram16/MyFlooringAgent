from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.cloud import storage
import PyPDF2
from io import BytesIO

# Google Cloud Storage Configuration
GCS_BUCKET_NAME = 'after5floor_rag'
GCS_FILE_NAME = 'AfterFiveFloors_Detailed_Profile.pdf'
PROJECT_ID = 'leafy-emblem-423800-g9'


def load_pdf_from_gcs(bucket_name: str, file_name: str) -> str:
    """Load and extract text from PDF stored in Google Cloud Storage"""
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        # Download PDF content
        pdf_content = blob.download_as_bytes()

        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()

        return text_content
    except Exception as e:
        print(f"Error loading PDF from GCS: {e}")
        return ""


# Load RAG context from GCS
rag_context = load_pdf_from_gcs(GCS_BUCKET_NAME, GCS_FILE_NAME)


def search_rag_knowledge_base(query: str) -> str:
    """Search the RAG knowledge base for relevant information"""
    if not rag_context:
        return "Knowledge base not available"

    # Use Gemini to search and extract relevant information from the PDF content
    #client = Client._nextgen_client

    search_prompt = f"""Given the following company information:

{rag_context}

Answer the user's question: {query}

Provide a concise and helpful answer based only on the information provided above."""

    return search_prompt


flooring_chat_agent_vertex_ai_search_agent = LlmAgent(
    name='Flooring_chat_agent_vertex_ai_search_agent',
    model='gemini-2.5-flash',
    description=(
        'Agent specialized in searching company information from RAG source.'
    ),
    sub_agents=[],
    instruction='Use the search_rag_knowledge_base tool to find information about AfterFiveFloors from the company profile document.',
    tools=[
        search_rag_knowledge_base
    ],
)

root_agent = LlmAgent(
    name='Flooring_chat_agent',
    model='gemini-2.5-flash',
    description=(
        'To chat with customers'
    ),
    sub_agents=[flooring_chat_agent_vertex_ai_search_agent],
    instruction='''You are a chat agent and your name is Aphia who will welcome customers on behalf of AfterFiveFloors, a flooring company. 

You have access to the company's detailed profile and information through the search_rag_knowledge_base tool. Use this tool to answer customer questions about the company, services, products, and offerings.

You will gather the customer name, email address and their house address and ask if you can book their appointment. Ask them for phone number.

Always refer to the company information from the RAG knowledge base when answering questions about AfterFiveFloors.''',
    tools=[
        search_rag_knowledge_base
    ],
)
