from .run import app
from .models import db, User, Task
from sqlalchemy import inspect

if __name__ == '__main__':
    with app.app_context():
        print("Using DB URI:", app.config.get('SQLALCHEMY_DATABASE_URI'))
        insp = inspect(db.engine)
        print("Tables in DB:", insp.get_table_names())
        try:
            users = User.query.all()
            print("Users count:", len(users))
            for u in users:
                print(u.id, u.username, u.email)
        except Exception as e:
            print("Error querying users:", e)

        try:
            tasks = Task.query.all()
            print("Tasks count:", len(tasks))
            for t in tasks:
                print(t.id, t.title, t.slug, t.user_id)
        except Exception as e:
            print("Error querying tasks:", e)