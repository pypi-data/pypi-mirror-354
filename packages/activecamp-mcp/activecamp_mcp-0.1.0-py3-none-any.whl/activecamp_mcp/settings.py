from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8080
    prometheus_port: int = 9090
    log_level: str = "INFO"
    reload: bool = False
    workers: int = 1

    mcp_dir: str = "/etc/fastmcp/"
    mcp_webhook_url: str = ""
    mcp_webhook_extra_data: dict = {}
    ac_api_url: str
    ac_api_token: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


settings = Settings()
