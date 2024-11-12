from fastapi import FastAPI

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

@app.get("/textmaster")
async def textmaster():
    return {"hello world"}

@app.get("/imagemaster")
async def imagemaster(item_id : int):
    return {"item_id":item_id}
