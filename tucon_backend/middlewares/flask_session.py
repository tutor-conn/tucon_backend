from tucon_backend import app
from tucon_backend.config import get_config
from redis import Redis
from flask_session.redis import RedisSessionInterface


config = get_config()
redis = Redis(
    host=config.UPSTASH_REDIS_HOST,
    port=config.UPSTASH_REDIS_PORT,
    password=config.UPSTASH_REDIS_PASSWORD,
    ssl=True,
)
app.config.update(
    # NOTE: '__session' is a special value that bypasses Firebase Hosting's cache
    # See https://firebase.google.com/docs/hosting/manage-cache#using_cookies
    SESSION_COOKIE_NAME="__session",
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
app.secret_key = config.FLASK_SECRET_KEY
app.session_interface = RedisSessionInterface(app=app, client=redis)
