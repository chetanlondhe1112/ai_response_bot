# Gemini LLM Algorithms Code 
from google import genai
from integrations_core import PineconeHandler

class AskGemini(PineconeHandler):

    def __init__(self,llm_config=object,vectordb_config=object):
        super().__init__(vectordb_config)
        self.__gemini_config = llm_config
        self.__api_key = self.__gemini_config['gemini_api_key']
        self.__model = self.__gemini_config['gemini_model']
        self.client = genai.Client(api_key=self.__api_key)
        self.gemini_model = self.client.models
        self.user_sessions={}
    
    async def get_user_session(self,user_id:str) -> list:
        """Retrieve or create a session for a user."""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []  # Create a new session if not exists
        return self.user_sessions[user_id]
    
    async def add_user_session_content(self,user_id:str,content:str) -> list:
        """Add sesssion content for a user."""
        if user_id in self.user_sessions:
            self.user_sessions[user_id].append(content)
        return self.user_sessions[user_id]
    
    def generate_text_content(self,query:str) -> object:
        return self.gemini_model.generate_content(
                    model=self.__model,
                    contents=query)

    def text_response(self,text_input:str) -> str:
        """_summary_
        Args:
            user_input (_type_): _description_
            prompt (_type_): _description_
        Returns:
            _type_: _description_
        """
        try:
            response = self.generate_text_content(query=text_input)
            
            return response.text
             
        except Exception as e:
            print(f"Failed to generate text response :{e}")
            return None
        
    async def generate_session_text_content(self,user:str,text_input:str,prompt:str):
        
        user_session = await self.get_user_session(user_id=user)
        
        content = f"Using this prompt : {prompt} and Current Conversation : {user_session} use this to generate response on this new Query : {text_input} ,if there is no Current conversation is available then generate your own reponse on this query"
        
        print(f"{user} : {text_input}")
        
        response = await self.generate_text_content(query=content)
                
        await self.add_user_session_content(user_id=user,content=f"User:{text_input}")
        await self.add_user_session_content(user_id=user,content=f"AI:{response.text}")
        return response
    
    async def generate_session_vectordb_text_content(self,user:str,text_input:str,prompt:str) -> str:
        user_session = await self.get_user_session(user_id=user)

        context = await self.retrive_similar(query=text_input,user=user)
        
        content = f"Using this prompt : {prompt}, Previous VectorDB stored Context :{context} and Current Conversation : {user_session} generate response on this user Query : {text_input} ,if there is no valid context or Current conversation is available then generate your own reponse on this query"
        
        print(f"{user} : {text_input}")
        print(f"Session_content : {user_session}")
        print(f"Vector_content : {context}")

        response = self.text_response(text_input=content)
        
        await self.upsert_vectors(text_type="query",text=text_input,user=user)
        await self.upsert_vectors(text_type="response",text=response,user=user)
        await self.add_user_session_content(user_id=user,content=f"User:{text_input}")
        await self.add_user_session_content(user_id=user,content=f"AI:{response}")

        return response
        
    async def image_response(self,image_input=object,prompt=str):
        """_summary_
        Args:
            image_input (_type_, optional): _description_. Defaults to object.
            prompt (_type_, optional): _description_. Defaults to str.
        """
        try:
            pass
         
        except Exception as e:
            print(f"Failed to generate image response : {e}")
            return None