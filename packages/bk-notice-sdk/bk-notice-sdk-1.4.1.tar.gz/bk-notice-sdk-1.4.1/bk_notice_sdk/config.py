import os

from django.conf import settings

stage = os.getenv("BKPAAS_ENVIRONMENT", "prod")
mapping = {"stag": "stage", "prod": "prod"}
# 默认设置
BK_NOTICE = {
    "STAGE": mapping.get(stage, "stage"),
    "BK_API_URL_TMPL": getattr(settings, "BK_API_URL_TMPL", None) or os.getenv("BK_API_URL_TMPL"),
    "BK_API_APP_CODE": getattr(settings, "APP_CODE", None) or os.getenv("BKPAAS_APP_ID"),
    "BK_API_SECRET_KEY": getattr(settings, "SECRET_KEY", None) or os.getenv("BKPAAS_APP_SECRET"),
    "PLATFORM": getattr(settings, "APP_CODE", None) or os.getenv("APP_CODE"),
    "ENTRANCE_URL": "notice/",
    "LANGUAGE_COOKIE_NAME": getattr(settings, "LANGUAGE_COOKIE_NAME", "blueking_language"),
    "DEFAULT_LANGUAGE": "en",
    "ENABLE_MULTI_TENANT_MODE": getattr(settings, "ENABLE_MULTI_TENANT_MODE", 0),
    "BK_APP_TENANT_ID": getattr(settings, "BK_APP_TENANT_ID", "system")
}

# 用户配置
USER_SETTING = getattr(settings, "BK_NOTICE", {})

# 合并后配置，以用户配置为主
bk_notice = BK_NOTICE.copy()
bk_notice.update(USER_SETTING)

for k, v in bk_notice.items():
    if v is None:
        raise ValueError(f"Missing BK_NOTICE settings: {k}")

# 版本
STAGE = bk_notice["STAGE"]

# apigw 请求相关配置
BK_API_URL_TMPL = bk_notice["BK_API_URL_TMPL"]
BK_API_APP_CODE = bk_notice["BK_API_APP_CODE"]
BK_API_SECRET_KEY = bk_notice["BK_API_SECRET_KEY"]

# 平台
PLATFORM = bk_notice["PLATFORM"]

# 入口URL
ENTRANCE_URL = bk_notice["ENTRANCE_URL"]

# 语言
LANGUAGE_COOKIE_NAME = bk_notice["LANGUAGE_COOKIE_NAME"]
# 默认语言
DEFAULT_LANGUAGE = bk_notice["DEFAULT_LANGUAGE"]

ENABLE_MULTI_TENANT_MODE = bk_notice["ENABLE_MULTI_TENANT_MODE"]
BK_APP_TENANT_ID = bk_notice["BK_APP_TENANT_ID"]
