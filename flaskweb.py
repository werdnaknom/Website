from config import DeploymentConfig, DevelopmentConfig
from app import create_app

app = create_app(config_class=DeploymentConfig)

globalConfig = DevelopmentConfig

if __name__ == "__main__":
    config = DevelopmentConfig
    app = create_app(config_class=config)

    app.run(debug=True)
