from fastapi import APIRouter, Request, UploadFile, File
from pathlib import Path
from pydantic import BaseModel
from routes.request import ChatRequest, SwitchModelRequest
from utils.api_response import ApiResponse
from utils.logger import logger
from repository.chat_repository import ChatRepository

router = APIRouter()
chat_repo = ChatRepository()

@router.post("/chat")
async def process_chat(request: Request, chat_request: ChatRequest):
    """Process a chat message using the currently loaded LLM"""
    llm_service = request.app.state.llm_service
    if not llm_service:
        return ApiResponse.fail(500, "LLM Service is not initialized")
        
    if not llm_service.is_initialized:
        return ApiResponse.fail(400, "No model loaded. Please load a model first.")

    try:
        answer = llm_service.get_response(chat_request.question)
        
        # Log transaction to PostgreSQL using Repository pattern
        chat_repo.save(
            model=llm_service.current_model or "Unknown",
            system_prompt="",
            input_text=chat_request.question,
            response_text=answer
        )
        
        return ApiResponse.success({"answer": answer})
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return ApiResponse.fail(500, str(e))


@router.post("/reset")
async def reset_chat(request: Request):
    """Reset the chat history memory"""
    llm_service = request.app.state.llm_service
    if not llm_service:
        return ApiResponse.fail(500, "LLM Service is not initialized")
        
    try:
        llm_service.reset_memory()
        return ApiResponse.success({"message": "Memory cleared successfully"})
    except Exception as e:
        logger.error(f"Error resetting memory: {e}")
        return ApiResponse.fail(500, str(e))


@router.get("/models")
async def list_models(request: Request):
    """List available models for the LLM Playground"""
    llm_service = request.app.state.llm_service
    if not llm_service:
        return ApiResponse.fail(500, "LLM Service is not initialized")
        
    models = llm_service.get_available_models()
    return ApiResponse.success({
        "models": models,
        "current_model": llm_service.current_model
    })


@router.post("/models/switch")
async def switch_model(request: Request, switch_request: SwitchModelRequest):
    """Switch the LLM model"""
    llm_service = request.app.state.llm_service
    if not llm_service:
        return ApiResponse.fail(500, "LLM Service is not initialized")
        
    try:
        llm_service.switch_model(switch_request.model_filename)
        return ApiResponse.success({
            "message": f"Successfully switched to {switch_request.model_filename}",
            "current_model": llm_service.current_model
        })
    except FileNotFoundError as e:
        return ApiResponse.fail(404, str(e))
    except Exception as e:
        logger.error(f"Error switching model: {e}")
        return ApiResponse.fail(500, str(e))


@router.post("/documents/upload")
async def upload_document(request: Request, file: UploadFile = File(...)):
    """Upload a PDF file and rebuild the vector store index for RAG"""
    from fastapi import UploadFile
    from core.config import settings
    import shutil
    
    llm_service = request.app.state.llm_service
    if not llm_service:
        return ApiResponse.fail(500, "LLM Service is not initialized")
        
    try:
        # Create documents directory if it doesn't exist
        doc_dir = Path(settings.data_path)
        doc_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file to the documents directory
        file_path = doc_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info(f"Saved document {file.filename} to {file_path}")
        
        # Trigger rebuild of the vector database
        llm_service.vector_store_service.rebuild_vector_store()
        
        # Re-initialize the LLM conversational chain with the new retriever
        llm_service._initialize_chain()
        
        return ApiResponse.success({
            "message": f"Successfully uploaded {file.filename} and rebuilt vector store index."
        })
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        return ApiResponse.fail(500, str(e))


@router.get("/documents")
async def list_documents():
    """List all uploaded PDF documents in settings.data_path"""
    from core.config import settings
    doc_dir = Path(settings.data_path)
    if not doc_dir.exists():
        return ApiResponse.success([])
    files = [f.name for f in doc_dir.glob("*.pdf")]
    return ApiResponse.success(files)


@router.delete("/documents/{filename}")
async def delete_document(filename: str, request: Request):
    """Delete a PDF document from context and rebuild vector store index"""
    from core.config import settings
    llm_service = request.app.state.llm_service
    if not llm_service:
        return ApiResponse.fail(500, "LLM Service is not initialized")
        
    try:
        doc_dir = Path(settings.data_path)
        file_path = doc_dir / filename
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Deleted document file: {filename}")
            
            # Rebuild vector database
            llm_service.vector_store_service.rebuild_vector_store()
            llm_service._initialize_chain()
            
            return ApiResponse.success({
                "message": f"Successfully deleted {filename} and rebuilt RAG index."
            })
        else:
            return ApiResponse.fail(404, f"Document {filename} not found.")
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        return ApiResponse.fail(500, str(e))


# Background Model Downloader Utilities and State
import threading
import urllib.request

download_status = {
    "active": False,
    "filename": "",
    "percentage": 0,
    "error": None
}

def start_download_thread(url: str, filename: str, models_dir: Path):
    global download_status
    try:
        download_status["active"] = True
        download_status["filename"] = filename
        download_status["percentage"] = 0
        download_status["error"] = None
        
        models_dir.mkdir(parents=True, exist_ok=True)
        file_path = models_dir / filename
        
        logger.info(f"Starting background model download from {url} to {file_path}")
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            total_size = int(response.info().get('Content-Length', 0))
            bytes_so_far = 0
            chunk_size = 1024 * 1024 # 1MB chunks
            
            with open(file_path, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_so_far += len(chunk)
                    if total_size > 0:
                        percent = int((bytes_so_far / total_size) * 100)
                        download_status["percentage"] = percent
                        
        logger.info(f"Model download successfully completed: {filename}")
        download_status["percentage"] = 100
        download_status["active"] = False
    except Exception as e:
        logger.error(f"Error during model download thread: {e}")
        download_status["error"] = str(e)
        download_status["active"] = False


class DownloadModelRequest(BaseModel):
    url: str
    filename: str


@router.post("/models/download")
async def download_model(request: Request, download_req: DownloadModelRequest):
    """Download a local LLM GGUF model in a background daemon thread"""
    global download_status
    if download_status["active"]:
        return ApiResponse.fail(400, "A model download is already in progress.")
        
    llm_service = request.app.state.llm_service
    if not llm_service:
        return ApiResponse.fail(500, "LLM Service is not initialized")
        
    thread = threading.Thread(
        target=start_download_thread,
        args=(download_req.url, download_req.filename, llm_service.models_dir)
    )
    thread.daemon = True
    thread.start()
    
    return ApiResponse.success({
        "message": f"Successfully started background download for model: {download_req.filename}"
    })


@router.get("/models/download/status")
async def get_download_status():
    """Fetch the status of any background model download"""
    global download_status
    return ApiResponse.success(download_status)
