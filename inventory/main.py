from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from pydantic_settings import BaseSettings

# Configuration
class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""

    class Config:
        env_file = ".env"

settings = Settings()

# FastAPI app
app = FastAPI(title="Inventory Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
redis = get_redis_connection(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password if settings.redis_password else None,
    decode_responses=True
)

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
    try:
        products = []
        for pk in Product.all_pks():
            product = Product.get(pk)
            products.append({
                "id": product.pk,
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity
            })
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")

@app.post("/products")
def create_product(product: Product):
    """Create a new product"""
    try:
        saved_product = product.save()
        return {
            "id": saved_product.pk,
            "name": saved_product.name,
            "price": saved_product.price,
            "quantity": saved_product.quantity
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

@app.get("/products/{product_id}")
def get_product(product_id: str):
    """Get a specific product by ID"""
    try:
        product = Product.get(product_id)
        return {
            "id": product.pk,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}")
def update_product(product_id: str, product_data: Product):
    """Update a product"""
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
    except Exception as e:
        raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    """Delete a product"""
    try:
        Product.delete(product_id)
        return {"message": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Product not found")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "inventory"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)