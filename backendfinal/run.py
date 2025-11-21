import os

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Allow overriding port via environment (useful when port 5000 is already used)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
