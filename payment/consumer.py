import time
from main import redis, Order

# Redis stream configuration
REFUND_STREAM = "refund_order"
CONSUMER_GROUP = "payment-group"

def setup_stream():
    """Setup Redis stream and consumer group"""
    try:
        redis.xgroup_create(REFUND_STREAM, CONSUMER_GROUP, mkstream=True)
        print("Redis stream and consumer group created successfully")
    except Exception as e:
        print(f"Stream/group already exists or error: {e}")

def process_refund_message(message_id, message_data):
    """Process a single refund message"""
    try:
        order_id = message_data.get("pk")
        
        if not order_id:
            print(f"Invalid refund message data: {message_data}")
            return False
        
        # Get order from Redis
        order = Order.get(order_id)
        
        # Update order status to refunded
        order.status = "refunded"
        order.save()
        
        print(f"Order {order_id} has been refunded successfully")
        return True
        
    except Exception as e:
        print(f"Error processing refund message {message_id}: {e}")
        return False

def main():
    """Main consumer loop"""
    print("Starting Payment Consumer...")
    setup_stream()
    
    while True:
        try:
            # Read messages from stream
            messages = redis.xreadgroup(
                CONSUMER_GROUP, 
                "payment-consumer", 
                {REFUND_STREAM: ">"}, 
                count=1, 
                block=1000  # Block for 1 second
            )
            
            if messages:
                for stream_name, stream_messages in messages:
                    for message_id, message_data in stream_messages:
                        # Process the refund message
                        success = process_refund_message(message_id, message_data)
                        
                        # Acknowledge message
                        redis.xack(REFUND_STREAM, CONSUMER_GROUP, message_id)
                        
                        if success:
                            print(f"Refund message {message_id} processed successfully")
                        else:
                            print(f"Refund message {message_id} processing failed")
                            
        except Exception as e:
            print(f"Error in consumer loop: {e}")
            time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    main()