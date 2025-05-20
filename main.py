from dotenv import load_dotenv
import os

# Load environment variables from .env file if it exists
load_dotenv()

from src.main import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
