import time
from .pinecone_setter import PINECONE

class PineconeHandler(PINECONE):

    def __init__(self,vectordb_config):
        super().__init__(vectordb_config)
        self.index,self.pc = self.create_index()
    
    async def query_embedding_retriver(self,query):
        # Convert the query into a numerical vector that Pinecone can search with
        query_embedding = self.pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[query],
            parameters={
                "input_type": "query"
            }
        )
        
        return query_embedding[0].values
        
    async def upsert_vectors(self,text_type:str,text:str,user:str):
        if len(text)<3:
            id_text=text
        else:
            id_text=text[:5]
        text_embedding = await self.query_embedding_retriver(text)
        vec = [
        {"id": f"{text_type}_{id_text}_{int(time.time())}", "values": text_embedding, 
        "metadata": {"{text_type}": text,"user":user}}
        ]
        
        self.index.upsert(
            vectors=vec,
            namespace="chatbot-namespace"
        )
    
    async def retrive_similar(self,query,user):
        
        # Search the index for the three most similar vectors
        results = self.index.query(
            namespace="chatbot-namespace",
            vector=await self.query_embedding_retriver(query),
            top_k=3,
            include_values=False,
            include_metadata=True,
            filter={"user": user}
        )
        return results
