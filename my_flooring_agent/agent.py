import openai
import google.cloud.storage

# Initialize the Google Cloud Storage client
client = google.cloud.storage.Client()

# Load the company profile document from Google Cloud Storage
bucket_name = 'after5floor_rag'
file_name = 'AfterFiveFloors_Detailed_Profile.pdf'

bucket = client.bucket(bucket_name)
document_blob = bucket.blob(file_name)
document_content = document_blob.download_as_text()  # Assuming it's a text-based PDF

class FlooringAgent:
    def __init__(self):
        pass

    def answer_question(self, question):
        # Use RAG integration to process the question and the content from the document
        response = openai.Completion.create(
            engine='davinci',
            prompt=f'Using the following document, answer the question: {question}\n\nDocument Content: {document_content}',
            max_tokens=150
        )
        return response.choices[0].text.strip()

# Example usage
agent = FlooringAgent()
question = "What services do you provide?"  # Replace with any customer question
answer = agent.answer_question(question)
print(answer)
