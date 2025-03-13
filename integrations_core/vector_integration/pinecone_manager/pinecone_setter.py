# Import the Pinecone library
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

class PINECONE:
    def __init__(self,vectordb_config):
        self.pc_api_key = vectordb_config['pinecone_api_key']
    
    def create_index(self):
        # Initialize a Pinecone client with your API key
        pc = Pinecone(api_key=self.pc_api_key)
        # Target the index where you'll store the vector embeddings
        INDEX_NAME = "gemini-chatbotv2"

        # Check if index exists, else create it
        if INDEX_NAME not in pc.list_indexes().names():
            pc.create_index(
                name=INDEX_NAME,
                dimension=1024,  # Based on Gemini embedding model
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )

        # Connect to index
        index = pc.Index(INDEX_NAME)
        return index,pc