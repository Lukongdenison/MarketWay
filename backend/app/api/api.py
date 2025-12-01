from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil

from app.services.data_loader import data_loader
from app.services.search_service import search_service
from app.services.voice_service import voice_service
from app.services.image_service import image_service
from app.services.navigation_service import navigation_service
from app.core.config import settings

router = APIRouter()

# --- Models ---
class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    source: str # 'local', 'online', 'combined'
    images: List[str] = []

class ProductSearchResponse(BaseModel):
    query: str
    results: List[dict]

class LineInfoResponse(BaseModel):
    line_name: str
    items_sold: List[str]
    layout: dict
    image_url: Optional[str]

class NavigateResponse(BaseModel):
    line_name: str
    directions: str
    layout: dict

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Answer general questions using local history, market data, and online search.
    """
    question = request.question.lower()
    
    # Extract potential product keywords from common question patterns
    # Remove common words to get the actual product name
    stop_words = ['i', 'want', 'to', 'buy', 'find', 'where', 'can', 'get', 'looking', 'for', 'need', 'a', 'an', 'the', 'some']
    words = question.split()
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    # 1. Check local data (simple keyword match for now)
    local_context = ""
    local_answer_parts = []
    found_images = []
    products = []
    
    # Check history
    if "history" in question or "built" in question or "old" in question:
        history_snippet = data_loader.get_history()[:500]
        if history_snippet:
            local_context += f"History Context: {history_snippet}... "
            local_answer_parts.append(f"According to market history: {history_snippet[:200]}...")
    
    # Search for products using extracted keywords
    for keyword in keywords:
        found_products = data_loader.search_products(keyword)
        if found_products:
            products.extend(found_products)
    
    # Remove duplicates
    if products:
        seen_lines = set()
        unique_products = []
        for p in products:
            if p['line_name'] not in seen_lines:
                unique_products.append(p)
                seen_lines.add(p['line_name'])
        products = unique_products
    
    if products:
        # Build detailed answer with directions
        line_details = []
        for line in products:
            line_name = line['line_name']
            column = line['layout']['column']
            order = line['layout']['order']
            items = ', '.join(line['items_sold'][:5])  # Show first 5 items
            
            line_details.append(f"{line_name} (located in the {column} column, position {order}) - sells {items}")
            
            # Find matching image
            if os.path.exists(settings.IMAGES_DIR):
                for img_file in os.listdir(settings.IMAGES_DIR):
                    if img_file.lower().startswith(line_name.lower()):
                        found_images.append(f"/images/{img_file}")
                        break
        
        # Create a helpful answer
        if len(products) == 1:
            answer = f"You can find that at {line_details[0]}."
        else:
            answer = f"You can find that at the following lines in Bamenda Main Market:\n\n" + "\n".join([f"• {detail}" for detail in line_details])
        
        return AskResponse(
            answer=answer,
            source="local",
            images=found_images
        )

    # 2. If no local products found, check if it's a general market question
    if not products and not local_answer_parts:
        # Only use online search as last resort
        search_query = f"{question}. Context: {local_context}" if local_context else question
        answer = search_service.search(search_query)
        
        return AskResponse(
            answer=answer,
            source="online" if not local_context else "combined",
            images=[]
        )
    
    # 3. Return local answer if we have history but no products
    if local_answer_parts:
        full_local_answer = " ".join(local_answer_parts)
        return AskResponse(
            answer=full_local_answer,
            source="local",
            images=found_images
        )

@router.get("/product/search", response_model=ProductSearchResponse)
async def search_product(q: str = Query(..., description="Product name to search for")):
    results = data_loader.search_products(q)
    
    # Add image URLs to each result
    for line in results:
        image_filename = None
        if os.path.exists(settings.IMAGES_DIR):
            for f in os.listdir(settings.IMAGES_DIR):
                if f.lower().startswith(line["line_name"].lower()):
                    image_filename = f
                    break
        line["image_url"] = f"/images/{image_filename}" if image_filename else None
    
    return ProductSearchResponse(query=q, results=results)

@router.get("/line/info/{line_name}", response_model=LineInfoResponse)
async def get_line_info(line_name: str):
    line = data_loader.get_line_by_name(line_name)
    if not line:
        raise HTTPException(status_code=404, detail="Line not found")
    
    # Construct image URL
    # Assuming images are served at /images/{Line Name}.jpg
    # We need to find the matching file since extension/casing might vary
    image_filename = None
    if os.path.exists(settings.IMAGES_DIR):
        for f in os.listdir(settings.IMAGES_DIR):
            if f.lower().startswith(line_name.lower()):
                image_filename = f
                break
    
    image_url = f"/images/{image_filename}" if image_filename else None

    return LineInfoResponse(
        line_name=line["line_name"],
        items_sold=line["items_sold"],
        layout=line["layout"],
        image_url=image_url
    )

@router.get("/history")
async def get_history():
    history = data_loader.get_history()
    return {"history": history}

@router.post("/voice/query")
async def voice_query(file: UploadFile = File(...)):
    # Save temp file
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # STT
    text = voice_service.speech_to_text(temp_path)
    
    # Cleanup input
    os.remove(temp_path)
    
    if not text:
        raise HTTPException(status_code=400, detail="Could not understand audio")

    # Process as a question (reuse logic or just return text)
    # For this endpoint, let's return the text and a spoken response to a simple search
    
    # Search for products
    products = data_loader.search_products(text)
    if products:
        response_text = f"I found {text} in {len(products)} lines: {', '.join([p['line_name'] for p in products[:3]])}"
    else:
        # Fallback to general search
        response_text = search_service.search(text)

    # TTS
    audio_response_path = voice_service.text_to_speech(response_text)
    
    return FileResponse(audio_response_path, media_type="audio/mpeg", filename="response.mp3")

@router.post("/image/identify")
async def identify_image(file: UploadFile = File(...)):
    contents = await file.read()
    result = image_service.identify_product(contents)
    return result

@router.get("/navigate", response_model=NavigateResponse)
async def navigate(line_name: str = Query(..., description="Target line name")):
    result = navigation_service.get_directions(line_name)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return NavigateResponse(**result)
