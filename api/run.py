from app import create_app
import os

# entry point of app and docker build
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_RUN_PORT"), debug=True)