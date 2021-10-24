import os
from app import celeryapp, create_app
from config import DevelopmentConfig, DeploymentConfig

app = create_app(config_class=DevelopmentConfig)
app.app_context().push()


# celeryapp.autodiscover_tasks()



