from main import function_3, function_4, function_5, logger, INDEX_DIR, TOP_K
import os
import json
import asyncio
from nats.aio.client import Client as NATS
from dotenv import load_dotenv


load_dotenv()
nats_url = os.getenv("NATS_URL", "nats://localhost:4222")
nats_subject = os.getenv("NATS_SUBJECT", "nats_subject")

async def connectRAG():
    nc = NATS()
    
    store = function_3(INDEX_DIR)
    
    try:
        await nc.connect(nats_url)
        print(f"NATS Connected on {nats_url}")
        
        async def message_handler(msg):
            data = json.loads(msg.data.decode())
            QUERY = data.get("query")
            print("Received prompt")
            
            results = function_4(store, QUERY, TOP_K)
            json_results = function_5(results, TOP_K)

            await msg.respond(json.dumps(json_results).encode())
            logger.info("Response send")
            
            for obj in json_results:
                filename = obj["filename"]
                print(f"Sent file : {filename}")
            
    except Exception as e:
        logger.error(f"Failed to connect to NATS: {e}")
        raise
    
    await nc.subscribe(nats_subject, cb=message_handler)
    while True:
        await asyncio.sleep(1)
        
if __name__ == "__main__":
        asyncio.run(connectRAG())
