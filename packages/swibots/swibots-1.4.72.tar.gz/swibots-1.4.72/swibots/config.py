import os


APP_CONFIG = {
    "CHAT_SERVICE": {
        "BASE_URL": os.getenv("CHAT_SERVICE_BASE_URL") or "https://chat-api.switchx.org",
        "WS_URL": os.getenv("CHAT_SERVICE_WS_URL")
        or "wss://chat-api.switchx.org/v1/websocket/message/ws",
    },
    "BOT_SERVICE": {
        "BASE_URL": os.getenv("BOT_SERVICE_BASE_URL") or "https://chat-api.switchx.org",
    },
    "AUTH_SERVICE": {
        "BASE_URL": os.getenv("AUTH_SERVICE_BASE_URL")
        or "https://gateway.switchx.org/user-service",
    },
    "AIRDROP_SERVICE": {
        "BASE_URL": os.getenv("AIRDROP_SERVICE_BASE_URL")
        or "https://gateway.switchx.org/airdrop-service"
    },
    "COMMUNITY_SERVICE": {
        "BASE_URL": os.getenv("COMMUNITY_SERVICE_BASE_URL")
        or "https://gateway.switchx.org/community-service",
        "WS_URL": os.getenv("COMMUNITY_SERVICE_WS_URL")
        or "wss://gateway.switchx.org/community-service/v1/websocket/community/ws",
    },
    "BACKBLAZE": {
        "BUCKET_ID": os.getenv("BACKBLAZE_BUCKET_ID") or "6e4a0369d05018689a560c1e",
        "ACCOUNT_ID": os.getenv("BACKBLAZE_ACCOUNT_ID") or "005ea390088a6ce0000000001",
        "APPLICATION_KEY": os.getenv("BACKBLAZE_APPLICATION_KEY") or "K005/dLxZIYBzJLms5IEZ7CnZJUBRCU",
    },
}


def get_config():
    return APP_CONFIG


def reload_config():
    APP_CONFIG["CHAT_SERVICE"]["BASE_URL"] = (
        os.getenv("CHAT_SERVICE_BASE_URL") or "https://chat-api.switchx.org"
    )
    APP_CONFIG["CHAT_SERVICE"]["WS_URL"] = (
        os.getenv("CHAT_SERVICE_WS_URL")
        or "wss://chat-api.switchx.org/v1/websocket/message/ws"
    )
    APP_CONFIG["BOT_SERVICE"]["BASE_URL"] = (
        os.getenv("BOT_SERVICE_BASE_URL") or "https://chat-api.switchx.org"
    )
    APP_CONFIG["AUTH_SERVICE"]["BASE_URL"] = (
        os.getenv("AUTH_SERVICE_BASE_URL") or "https://gateway.switchx.org/user-service"
    )
    APP_CONFIG["COMMUNITY_SERVICE"]["BASE_URL"] = (
        os.getenv("COMMUNITY_SERVICE_BASE_URL")
        or "https://gateway.switchx.org/community-service"
    )
    APP_CONFIG["COMMUNITY_SERVICE"]["WS_URL"] = (
        os.getenv("COMMUNITY_SERVICE_WS_URL")
        or "wss://gateway.switchx.org/community-service/v1/websocket/community/ws"
    )
    APP_CONFIG["AIRDROP_SERVICE"]["BASE_URL"] = (
        os.getenv("AIRDROP_SERVICE_BASE_URL")
        or "https://gateway.switchx.org/airdrop-service"
    )


reload_config()
