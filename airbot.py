from fastapi import FastAPI,File,Form,UploadFile
import os
import airbot_integration_core as aic
from llm_algo.llm_models import airbotllm
import json

app = FastAPI(title="AIRBOT : AI Response BOT Service API's",
    description="""
    Background : 
    The AIRBOT Service is designed to enhance the performance and responsiveness of Smartchat by addressing the latency challenges posed by the AI LLM (Large Language Model) integrations. In the current setup, AI LLM models within Smartchat result in slower response times due to high processing demands, impacting the user experience.

    Solution Overview:
    To mitigate these issues, AIRBOT has been developed to offload the AI LLM processing from Smartchat’s core views, making the model available as a separate, high-performance API. This setup allows Smartchat to send user queries to AIRBOT asynchronously, enabling faster response times and smoother interactions.

    Key Benefits:
    Improved Performance: Offloading AI processing reduces the response latency within Smartchat, enhancing the user experience.
    Asynchronous Processing: AIRBOT enables asynchronous handling of queries, allowing Smartchat to remain responsive while waiting for results from the LLM models.
    Scalability: The separation of services provides scalability, as AIRBOT can be scaled independently to handle increased loads without impacting Smartchat directly.
    AIRBOT is designed as a seamless solution for efficient AI-driven query processing, ensuring that users experience rapid and reliable responses in Smartchat.""",
    version="1.0.0",
    contact={
        "name": "Support Team",
        "email": "chetanlondhe1112@gmail.com",
    })

# Load Config path
script_dir = os.getcwd()
print(script_dir)
config_path = os.path.join(script_dir,"conf\conf.toml")
config_status,config = aic.load_config(filepath=config_path)

airbotllm = airbotllm(llmconfig=config['airbotllm'])

#Prompts
smartchat_prompt_path = os.path.join(script_dir,"prompts\smartchat_prompts.toml")
_,smartchatapp_prompts = config = aic.load_config(filepath=smartchat_prompt_path)

smartchatapp = aic.SmartchatModules(llmmodel=airbotllm,smartchatprompts=smartchatapp_prompts)

@app.post("/textmaster/")
async def textmaster(text_question : str = Form(...), requestor : str = Form(...), arguments : str = Form(...)):
    print(text_question)
    if requestor == "smartchat":
        arguments = json.loads(arguments)
        result = await smartchatapp.modules(text_input=text_question,image_input=None,class_name=arguments['class_name'],module_name=arguments['module_name'],request_format="text")
        return {"result":result}
    

@app.get("/imagemaster/")
async def imagemaster(item_id : int):
    return {"item_id":item_id}
