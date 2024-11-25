from app.migration import run_migrations
from app import create_app

app = create_app()

# lastly, running the app
if __name__ == "__main__":
    run_migrations()
    app.run(debug=True)