from celery import Celery

# generate celery instance like other extension instances

celery = Celery(
    __name__, broker="redis://localhost:6379", backend="redis://localhost:6379"
)
