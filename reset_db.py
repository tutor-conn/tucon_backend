from dotenv import load_dotenv

load_dotenv()

from tucon_backend.db import get_engine

engine = get_engine()

from tucon_backend.models import Base

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
