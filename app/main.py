import sys
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import services
from app.services.crawler import CrawlerService
from app.services.generator import GeneratorService, BlogPost

# Load env vars early to ensure standard OpenAI vars are populated before services init
load_dotenv()

# Fix for Windows asyncio loop with Playwright
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Global service instances
crawler_service: CrawlerService = None
generator_service: GeneratorService = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global crawler_service, generator_service
    try:
        crawler_service = CrawlerService()
        generator_service = GeneratorService()
        print("Services initialized.")
    except Exception as e:
        print(f"Failed to initialize services: {e}")
    
    yield
    
    # Shutdown
    print("Shutting down services...")

app = FastAPI(title="URL to Blog Converter", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConvertRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the URL to Blog Converter API"}

@app.post("/convert", response_model=BlogPost)
async def convert_url(request: ConvertRequest):
    if not crawler_service or not generator_service:
        raise HTTPException(status_code=500, detail="Services not initialized")

    # 1. Crawl
    markdown_content = await crawler_service.crawl(request.url)
    if not markdown_content:
        raise HTTPException(status_code=400, detail="Failed to crawl URL or content is empty.")

    # 2. Generate
    try:
        blog_post = await generator_service.generate_blog(markdown_content)
        return blog_post
    except Exception as e:
        print(f"Error generating blog: {e}")
        # Return 500 but include error msg for debugging
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
