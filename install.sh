#!/bin/bash

echo "Setting up Stickt..."

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

if [ ! -f .env ]; then
    echo "REPLICATE_API_TOKEN=your_token_here" > .env
    echo "Created .env file - please add your Replicate API token"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Replicate API token"
echo "2. Run: source venv/bin/activate && python icky.py"
