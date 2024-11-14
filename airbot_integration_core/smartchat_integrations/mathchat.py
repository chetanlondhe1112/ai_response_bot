

class Mathchat_response:
    
    def __init__(self,prompts=dict,llm_model=object):
        self.llm_model = llm_model
        self.prompts = prompts
        self.question_grader_prompt = self.prompts['question_grader']
    
    async def image_mathchat(self,class_name,image_content):
        """
        Mathchat - Function Designed to collect the response of gemini-pro-vision self.model on image content 
        which will have mathematical problmes in it,for smartchat's Mathchat module.
        -Output: (response.text,math_answer,math_syllabus,answer_topics)
        """
        try:
            question_grader=self.question_grader_prompt.format(class_name)
            
            # Image response
            response = self.llm_model.image_response(image_content,self.prompts["mathchat_response_prompt"])
            
            # Text response
            math_answer = await self.llm_model.text_response(response.text,
                                                            self.prompts['mathchat_answer_prompt'].format(class_name)
                                                            )
            math_syllabus = await self.llm_model.text_response(math_answer,self.prompts['answer_syllabus_prompt'])
            answer_topics = await self.llm_model.text_response(math_answer,self.prompts['answer_topic_prompt'])
            question_rank = await self.llm_model.text_response(response.text,question_grader)
                    
            return {"response":response.text,"math_answer":math_answer,"math_syllabus":math_syllabus,      "answer_topics":answer_topics,"question_rank":question_rank}
        
        except Exception as e:
            
            print(f"Error to generate image response : {e}")
            return None

    async def text_mathchat(self,class_name,text_content):
        """
        Mathchat - Function Designed to collect the response of gemini-pro-vision self.model on image content 
        which will have mathematical problmes in it,for smartchat's Mathchat module.
        -Output: (response.text,math_answer,math_syllabus,answer_topics)
        """
        try:
            question_grader=self.question_grader_prompt.format(class_name)
            
            response = await self.llm_model.text_response(text_content,
                                                          self.prompts['mathchat_text_response_prompt'])
            math_answer = await self.llm_model.text_response(response,
                                                                self.prompts['mathchat_answer_prompt'])
            answer_topics = await self.llm_model.text_response(math_answer,
                                                               self.prompts['answer_topic_prompt'])
            math_syllabus = await self.llm_model.text_response(text_content,
                                                               self.prompts['answer_syllabus_prompt'])
            question_rank = await self.llm_model.text_response(response,question_grader)

            return {"response":response,"math_answer":math_answer,"math_syllabus":math_syllabus,"answer_topics":answer_topics,"question_rank":question_rank}
        
        except Exception as e:
            
            print(f"Error to generate Text response : {e}")
            return {}
