#!/bin/bash

echo "Setting up Quick Sell Wholesaler..."

echo ""
echo "Setting up Inventory Service..."
cd inventory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo ""
echo "Setting up Payment Service..."
cd payment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo ""
echo "Setting up Frontend..."
cd frontend
npm install
cd ..

echo ""
echo "Setup complete! Make sure Redis is running before starting the services."
echo "Run ./start-services.sh to start all services."
