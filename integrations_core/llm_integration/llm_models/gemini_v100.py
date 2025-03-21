# Gemini LLM Algorithms Code 
# Import
import google.generativeai as genai

class AskGemini:

    def __init__(self,gemini_config=object):
        self.__gemini_config = gemini_config
        self.__api_key = self.__gemini_config['gemini_api_key']
        self.model = self.__gemini_config['gemini_model']
        # GEMINI Configuration
        genai.configure(api_key=self.__api_key)
        self.model = genai.GenerativeModel(self.model)

    async def text_response(self,text_input=str,prompt=str):
        """_summary_
        Args:
            user_input (_type_): _description_
            prompt (_type_): _description_
        Returns:
            _type_: _description_
        """
        try:
            messages=[{'role':'user',
                            'parts':[str(prompt) + str(text_input)]}]
            response = self.model.generate_content(messages)
            return response.text
        except Exception as e:
            print(f"Failed to generate text response :{e}")
            return None

    async def image_response(self,image_input=object,prompt=str):
        """_summary_
        Args:
            image_input (_type_, optional): _description_. Defaults to object.
            prompt (_type_, optional): _description_. Defaults to str.
        """
        try:
            return await self.model.generate_content([prompt,image_input])
         
        except Exception as e:
            print(f"Failed to generate image response : {e}")
            return None