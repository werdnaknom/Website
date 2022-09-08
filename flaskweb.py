from config import DeploymentConfig, DevelopmentConfig
from app import create_app

#DEPLOYMENT CONFIG
app = create_app(config_class=DeploymentConfig)

globalConfig = DeploymentConfig

if __name__ == "__main__":
    #DEVELOPMENT CONFIG
    config = DevelopmentConfig
    app = create_app(config_class=config)

    app.run(debug=True)
