import time
from main import redis, Product

# Redis stream configuration
ORDER_STREAM = "order_completed"
CONSUMER_GROUP = "inventory-group"

def setup_stream():
    """Setup Redis stream and consumer group"""
    try:
        redis.xgroup_create(ORDER_STREAM, CONSUMER_GROUP, mkstream=True)
        print("Redis stream and consumer group created successfully")
    except Exception as e:
        print(f"Stream/group already exists or error: {e}")

def process_order_message(message_id, message_data):
    """Process a single order message"""
    try:
        product_id = message_data.get("product_id")
        quantity = int(message_data.get("quantity", 0))
        
        if not product_id or quantity <= 0:
            print(f"Invalid message data: {message_data}")
            return False
        
        # Get product from Redis
        product = Product.get(product_id)
        
        # Check if enough stock
        if product.quantity >= quantity:
            # Reduce stock
            product.quantity -= quantity
            product.save()
            print(f"Product {product_id} stock reduced by {quantity}. New quantity: {product.quantity}")
            return True
        else:
            # Not enough stock - trigger refund
            print(f"Insufficient stock for product {product_id}. Triggering refund.")
            redis.xadd("refund_order", message_data, "*")
            return True
            
    except Exception as e:
        print(f"Error processing message {message_id}: {e}")
        return False

def main():
    """Main consumer loop"""
    print("Starting Inventory Consumer...")
    setup_stream()
    
    while True:
        try:
            # Read messages from stream
            messages = redis.xreadgroup(
                CONSUMER_GROUP, 
                "inventory-consumer", 
                {ORDER_STREAM: ">"}, 
                count=1, 
                block=1000  # Block for 1 second
            )
            
            if messages:
                for stream_name, stream_messages in messages:
                    for message_id, message_data in stream_messages:
                        # Process the message
                        success = process_order_message(message_id, message_data)
                        
                        # Acknowledge message
                        redis.xack(ORDER_STREAM, CONSUMER_GROUP, message_id)
                        
                        if success:
                            print(f"Message {message_id} processed successfully")
                        else:
                            print(f"Message {message_id} processing failed")
                            
        except Exception as e:
            print(f"Error in consumer loop: {e}")
            time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    main()