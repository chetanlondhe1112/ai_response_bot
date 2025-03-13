from integrations_core import airbotllm

class ChatBotHandler(airbotllm):

    def __init__(self,llm_config=object,vectordb_config=object):
        super().__init__(llm_config,vectordb_config)
        self.gem = airbotllm(llm_config=llm_config,vectordb_config=vectordb_config)

    async def chatbot_response(self,text_content,user,prompt):
        """
        Chatbot - Function Designed to collect the response of gemini-pro-vision self.model on text content 
        -Output: (response.text)
        """
        #try:
        print()
        response = await self.gem.generate_session_vectordb_text_content(text_input=text_content,user=user,prompt=prompt)
        return {"response":response}
        #except Exception as e:
        #    print(f"Error to generate Text response : {e}")
        #    return {}

    async def upsert_content_to_vectordb(self,text_content,user):
        """
        Chatbot - Function Designed to collect the response of gemini-pro-vision self.model on text content 
        -Output: (response.text)
        """
        try:
            await self.gem.upsert_vectors(text_type="conversation",text=text_content,user=user)
            return {"response":True}
        except Exception as e:
            print(f"Error to upsert content : {e}")
            return {"response":False}