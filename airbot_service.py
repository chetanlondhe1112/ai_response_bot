from fastapi import FastAPI,Form
from fastapi.middleware.cors import CORSMiddleware
import os
import integrations_core as aic
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

# Define allowed origins
origins = [
    "http://127.0.0.1:8005",  # Replace with specific allowed origins
]

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specified origins
    allow_credentials=True,  # Allow credentials (if required)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load Config path
script_dir = os.getcwd()
config_path = os.path.join(script_dir,"conf/conf.toml")
#Prompts
smartchat_prompt_path = os.path.join(script_dir,"prompts/smartchat_prompts.toml")
chatbot_prompt_path = os.path.join(script_dir,"prompts/chatbot_prompts.toml")

config_loader = aic.ConfigLoader()
config=config_loader.get_config(config_path)
smartchatapp_prompts  = config_loader.get_config(smartchat_prompt_path)
chatbot_prompts  =  config_loader.get_config(chatbot_prompt_path)

llm_conf = config['airbotllm']
pinecone_conf = config['pinecone']

airbotllm = aic.airbotllm(llm_config=llm_conf,vectordb_config=pinecone_conf)
smartchatapp = aic.SmartchatModules(llmmodel=airbotllm,smartchatprompts=smartchatapp_prompts)
chatbotapp = aic.ChatBotHandler(llm_config=llm_conf,vectordb_config=pinecone_conf)




@app.post("/login/")
async def login():
    return {"result":''}

@app.post("/registration/")
async def registration():
    return {"result":''}

@app.post("/chatbot/")
async def chatbot(text_question : str = Form(...), requestor : str = Form(...)):
    
    result = await chatbotapp.chatbot_response(text_content=text_question,user=requestor,prompt="Act Like a chatbot and answer users query in deapth, and provide the relatedf citations like refernece links at end")
    print({"result":result})
    return {"result":result}

@app.post("/upsertcontext/")
async def upsertcontext(text:str=Form(...),user:str=Form(...)):
    result = await chatbotapp.upsert_content_to_vectordb(text_content=text,user=user)
    return {"result":result}

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
