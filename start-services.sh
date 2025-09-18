#!/bin/bash

echo "Starting Quick Sell Wholesaler Services..."

echo ""
echo "Starting Inventory Service..."
gnome-terminal --title="Inventory Service" -- bash -c "cd inventory && source venv/bin/activate && uvicorn main:app --reload --port 8000; exec bash"

echo ""
echo "Starting Payment Service..."
gnome-terminal --title="Payment Service" -- bash -c "cd payment && source venv/bin/activate && uvicorn main:app --reload --port 8001; exec bash"

echo ""
echo "Starting Frontend..."
gnome-terminal --title="Frontend" -- bash -c "cd frontend && npm start; exec bash"

echo ""
echo "Starting Inventory Consumer..."
gnome-terminal --title="Inventory Consumer" -- bash -c "cd inventory && source venv/bin/activate && python consumer.py; exec bash"

echo ""
echo "Starting Payment Consumer..."
gnome-terminal --title="Payment Consumer" -- bash -c "cd payment && source venv/bin/activate && python consumer.py; exec bash"

echo ""
echo "All services started! Check the opened terminals for logs."
echo "Frontend will be available at: http://localhost:3000"
echo "Inventory API will be available at: http://localhost:8000"
echo "Payment API will be available at: http://localhost:8001"
