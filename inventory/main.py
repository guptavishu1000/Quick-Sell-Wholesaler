from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from pydantic_settings import BaseSettings
import logging
from dotenv import load_dotenv
import os
from typing import Optional 

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
class Settings(BaseSettings):
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT"))
    redis_password: Optional[str] = os.getenv("REDIS_PASSWORD", None)
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# FastAPI app
app = FastAPI(title="Inventory Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:8000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
try:
    redis = get_redis_connection(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password if settings.redis_password else None,
        decode_responses=True
    )
    redis.ping()
    logger.info("Successfully connected to Redis.")
except Exception as e:
    logger.error(f"Could not connect to Redis: {e}")
    # You might want to exit or handle this more gracefully
    # For now, we'll let it fail on requests
    redis = None

# Product model
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

# API endpoints
@app.get("/products")
def get_all_products():
    """Get all products"""
    if not redis:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    try:
        products = []
        for pk in Product.all_pks():
            try:
                product = Product.get(pk)
                products.append({
                    "id": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "quantity": product.quantity
                })
            except Exception as e:
                logger.error(f"Error fetching product with pk {pk}: {e}")
                continue
        return products
    except Exception as e:
        logger.error(f"Error fetching all products: {e}")
        raise HTTPException(status_code=500, detail="Error fetching products")

@app.post("/products")
def create_product(product: Product):
    """Create a new product"""
    if not redis:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    try:
        saved_product = product.save()
        return {
            "id": saved_product.pk,
            "name": saved_product.name,
            "price": saved_product.price,
            "quantity": saved_product.quantity
        }
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Error creating product")

@app.get("/products/{product_id}")
def get_product(product_id: str):
    """Get a specific product by ID"""
    try:
        product = Product.get(product_id)
        product_dict = product.dict()
        product_dict['id'] = product.pk
        return product_dict
    except Exception:
        raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}")
def update_product(product_id: str, product_data: Product):
    """Update a product"""
    if not redis:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    try:
        product = Product.get(product_id)
        product.name = product_data.name
        product.price = product_data.price
        product.quantity = product_data.quantity
        saved_product = product.save()
        
        return {
            "id": saved_product.pk,
            "name": saved_product.name,
            "price": saved_product.price,
            "quantity": saved_product.quantity
        }
    except Exception:
        raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    """Delete a product"""
    if not redis:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    try:
        Product.delete(product_id)
        return {"message": "Product deleted successfully"}
    except Exception:
        raise HTTPException(status_code=404, detail="Product not found")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "inventory"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)