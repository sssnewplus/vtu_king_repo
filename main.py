from app.migration import run_migrations
from app import create_app, db
from app.models import User

app = create_app()

# # init the super_user
# with app.app_context():
#     super_user = User.query.filter_by(username='sssnew').first()
#     print(super_user)

# lastly, running the app
if __name__ == "__main__":
    run_migrations()
    app.run(debug=True)