# Quick Sell Wholesaler

A clean, production-ready microservices e-commerce application with Redis-based data persistence and real-time synchronization.

## 🏗️ Architecture

- **Frontend**: React application with Bootstrap UI
- **Inventory Service**: Product management (FastAPI + Redis)
- **Payment Service**: Order processing (FastAPI + Redis)
- **Redis**: Data storage and message streaming
- **Redis Streams**: Real-time event processing

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Redis server

### 1. Install Redis
```bash
# Windows (using Chocolatey)
choco install redis-64

# Or download from: https://github.com/microsoftarchive/redis/releases
```

### 2. Start Redis
```bash
redis-server
```

### 3. Setup Application
```bash
# Install all dependencies
setup.bat

# Start all services
start-services.bat
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Inventory API**: http://localhost:8000
- **Payment API**: http://localhost:8001

## 📋 Features

### ✅ Clean Code Architecture
- **Modular Design**: Separate services with clear responsibilities
- **Error Handling**: Comprehensive error handling and validation
- **Type Safety**: Pydantic models for data validation
- **Documentation**: Clear API documentation with FastAPI

### ✅ Redis Integration
- **Data Persistence**: All data stored in Redis
- **Real-time Sync**: Redis streams for event processing
- **Multi-user Support**: Concurrent access with data consistency
- **Atomic Operations**: Race condition prevention

### ✅ Product Management
- **CRUD Operations**: Create, read, update, delete products
- **Stock Management**: Real-time inventory tracking
- **No Auto-delete**: Products remain even when quantity is 0
- **Manual Deletion**: Only deleted via UI action

### ✅ Order Processing
- **Stock Validation**: Prevents overselling
- **Background Processing**: Asynchronous payment simulation
- **Status Tracking**: pending → completed → refunded
- **Fee Calculation**: Automatic 20% fee addition

## 🔧 API Endpoints

### Inventory Service (Port 8000)
```
GET    /products          # List all products
POST   /products          # Create product
GET    /products/{id}     # Get product
PUT    /products/{id}     # Update product
DELETE /products/{id}     # Delete product
GET    /health           # Health check
```

### Payment Service (Port 8001)
```
POST   /orders           # Create order
GET    /orders/{id}      # Get order
GET    /health          # Health check
```

## 🎯 Usage Flow

1. **Add Products**: Use the "Add" button to create products
2. **View Inventory**: See all products with current stock levels
3. **Place Orders**: Select product from dropdown and enter quantity
4. **Real-time Updates**: Stock reduces immediately after order
5. **Order Tracking**: Orders process in background (2-second delay)

## 🔄 Redis Streams

### Inventory Consumer
- Listens to `order_completed` stream
- Processes stock reductions
- Handles insufficient stock scenarios

### Payment Consumer
- Listens to `refund_order` stream
- Processes refund requests
- Updates order status

## 🛠️ Development

### Manual Service Start
```bash
# Inventory Service
cd inventory
venv\Scripts\activate
uvicorn main:app --reload --port 8000

# Payment Service
cd payment
venv\Scripts\activate
uvicorn main:app --reload --port 8001

# Frontend
cd frontend
npm start

# Consumers
cd inventory && python consumer.py
cd payment && python consumer.py
```

### Environment Configuration
Create `.env` files in service directories:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
INVENTORY_SERVICE_URL=http://localhost:8000
```

## 📊 Data Models

### Product
```json
{
  "id": "uuid",
  "name": "string",
  "price": "float",
  "quantity": "int"
}
```

### Order
```json
{
  "id": "uuid",
  "product_id": "string",
  "price": "float",
  "fee": "float",
  "total": "float",
  "quantity": "int",
  "status": "pending|completed|refunded"
}
```

## 🎉 Production Ready

- ✅ Clean, maintainable code
- ✅ Comprehensive error handling
- ✅ Redis-based data persistence
- ✅ Multi-user synchronization
- ✅ Real-time updates
- ✅ Background processing
- ✅ Health check endpoints
- ✅ Proper logging