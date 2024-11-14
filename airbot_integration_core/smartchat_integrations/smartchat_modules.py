# Integration for smartchat
from .mathchat import Mathchat_response

class SmartchatModules:
    
    def __init__(self,llmmodel,smartchatprompts):
        self.model = llmmodel
        self.smartchatprompts = smartchatprompts
        self.mathchat_prompts = self.smartchatprompts['mathchat_prompts']
        self.mathchat = Mathchat_response(prompts=self.mathchat_prompts,llm_model=self.model)
    
    async def modules(self,text_input=str,image_input=object,class_name=str,module_name=str,request_format=str):
        """

        Args:
            module_name (_type_, optional): _description_. Defaults to str.
            request_format (_type_, optional): _description_. Defaults to str.
        """
        try:
            if module_name == 'mathchat':
                if request_format == 'text':
                    
                    return await self.mathchat.text_mathchat(class_name=class_name,text_content=text_input)
                    
                elif request_format == 'image':
                    return await self.mathchat.image_mathchat(class_name=class_name,image_content=image_input)
                    
        except Exception as e:
            print(f"Error to Generate Response : {e}")
            return None
            
        
    