from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from pydantic_settings import BaseSettings
from starlette.requests import Request
import httpx
import time

# Configuration
class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    inventory_service_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"

settings = Settings()

# FastAPI app
app = FastAPI(title="Payment Service", version="1.0.0")

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

# Order model
class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis

# HTTP client for inventory service
client = httpx.AsyncClient()

# API endpoints
@app.get("/orders/{order_id}")
def get_order(order_id: str):
    """Get a specific order by ID"""
    try:
        order = Order.get(order_id)
        return {
            "id": order.pk,
            "product_id": order.product_id,
            "price": order.price,
            "fee": order.fee,
            "total": order.total,
            "quantity": order.quantity,
            "status": order.status
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Order not found")

@app.post("/orders")
async def create_order(request: Request, background_tasks: BackgroundTasks):
    """Create a new order"""
    try:
        # Parse request body
        body = await request.json()
        
        # Validate required fields
        if "id" not in body or "quantity" not in body:
            raise HTTPException(status_code=400, detail="Missing required fields: id and quantity")
        
        product_id = body["id"]
        quantity = int(body["quantity"])
        
        if quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

        # Get product details from inventory service
        try:
            response = await client.get(f"{settings.inventory_service_url}/products/{product_id}")
            response.raise_for_status()
            product = response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Product not found")
            else:
                raise HTTPException(status_code=503, detail=f"Inventory service error: {e.response.status_code}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Inventory service unavailable: {e}")

        # Check stock availability
        if product["quantity"] < quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough stock available. Only {product['quantity']} units in stock."
            )

        # Create order
        order = Order(
            product_id=product_id,
            price=product["price"],
            fee=0.2 * product["price"],  # 20% fee
            total=1.2 * product["price"],  # price + fee
            quantity=quantity,
            status="pending"
        )
        saved_order = order.save()

        # Update inventory (reduce stock)
        try:
            updated_product = {
                "name": product["name"],
                "price": product["price"],
                "quantity": product["quantity"] - quantity
            }
            
            update_response = await client.put(
                f"{settings.inventory_service_url}/products/{product_id}",
                json=updated_product
            )
            update_response.raise_for_status()
            
        except Exception as e:
            print(f"Warning: Failed to update inventory: {e}")

        # Process payment in background
        background_tasks.add_task(process_payment, saved_order.pk)
        
        return {
            "id": saved_order.pk,
            "product_id": saved_order.product_id,
            "price": saved_order.price,
            "fee": saved_order.fee,
            "total": saved_order.total,
            "quantity": saved_order.quantity,
            "status": saved_order.status
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid quantity format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def process_payment(order_id: str):
    """Process payment in background"""
    try:
        time.sleep(2)  # Simulate payment processing
        
        order = Order.get(order_id)
        order.status = "completed"
        order.save()
        
        print(f"Order {order_id} completed successfully!")
        
    except Exception as e:
        print(f"Error processing payment for order {order_id}: {e}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "payment"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)