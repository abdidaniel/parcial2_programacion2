from run import app, db
from models import User

with app.app_context():
    try:
        # Test connection
        db.engine.execute('SELECT 1')
        print("✅ DB Connection OK")
        
        # Check users
        users = User.query.all()
        print(f"\nUsers in database: {len(users)}")
        for user in users:
            print(f"- {user.username} ({user.email})")
    except Exception as e:
        print(f"❌ Error: {e}")