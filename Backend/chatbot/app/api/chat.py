from fastapi import APIRouter, Form, UploadFile, File
from app.services.ollama_service import process_image_with_ollama, process_text_with_ollama
from app.services.chat_history_service import get_chat_history, save_chat_history
from app.core import config, constants
import base64
import httpx

router = APIRouter()

@router.post(constants.CHAT_ROUTE_URL)
async def chat_with_ollama(prompt: str = Form(...), image: UploadFile = File(None), context: str = Form(None)):
    model = config.OLLAMA_MODEL
    
    history = get_chat_history()
    history.append({"role": "user", "content": prompt})
    print("Prompt: "+prompt)
    
    try:
        if image:
            contents = await image.read()
            image_b64 = base64.b64encode(contents).decode("utf-8")
            response = await process_image_with_ollama(model, history, prompt, image=image_b64)
        else:
            response = await process_text_with_ollama(model, history, prompt, context=context)
    except httpx.ReadTimeout:
        return {"response": constants.TIME_OUT_OLLAMA_MSSG}
    except Exception as e:
        print("Exception occured at get ollama response service: "+str(e))
        return {"response": constants.INTERNAL_SERVER_ERROR}
    
    print("DEBUG response:", response, type(response))
    
    history.append({"role": "assistant", "content": response["response"]})
    save_chat_history(history)
    
    return response