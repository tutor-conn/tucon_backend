from dotenv import load_dotenv

load_dotenv()

from tucon_backend.db import get_engine
from tucon_backend.middlewares.flask_session import redis

engine = get_engine()

from tucon_backend.models import Base

print("Dropping all tables...")
Base.metadata.drop_all(engine)

print("Creating all tables...")
Base.metadata.create_all(engine)

print("Clearing Redis...")
redis.flushall()
