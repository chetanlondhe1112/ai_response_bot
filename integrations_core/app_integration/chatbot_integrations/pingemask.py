from .pincone_manager import PineconeHandler

class GeminiASK(PineconeHandler):
    def __init__(self,model,index,pc):
        super().__init__(index,pc)
        self.pc=pc
        self.user_sessions={}
        self.model = model
        self.session = self.get_user_session(user_id=self.user)

    async def get_user_session(self,user_id):
        """Retrieve or create a session for a user."""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []  # Create a new session if not exists
        return self.user_sessions[user_id]
    
    async def add_data_to_user_session(self,user_id,data):
        self.user_sessions
        
    async def get_content(self,query):
        return self.model.generate_content(
                    model="gemini-2.0-flash",
                    contents=query)
    
    async def  generate_content(self,query):
        context = self.retrive_similar(query=query)
        content = f"""Previous Context :{context} ,Current Conversation : {self.session} 
        use this to generate response on this new Query : {query} ,if there is no valid 
        context or Current conversation is available then generate your own reponse on this query"""
        
        response = self.get_content(query=content)
        self.upsert_vectors(query=query,response=response.text)
        self.session.append(f"User:{query}")
        self.session.append(f"AI:{response}")

        return response
    
    
