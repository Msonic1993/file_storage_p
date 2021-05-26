from decouple import config

MYSQL_DATABASE = config('MYSQL_DATABASE', default='filestorage')
MYSQL_USER = config('MYSQL_USER', default='root')
MYSQL_PASSWORD = config('MYSQL_PASSWORD', default='')
MYSQL_HOST = config('MYSQL_HOST', default='localhost')
MYSQL_PORT = config('MYSQL_PORT', default=3306, cast=int)

OAUTH_SECRET_KEY = config('OAUTH_SECRET_KEY', default='')
OAUTH_OIDC_CLIENT_SECRETS = config('OAUTH_OIDC_CLIENT_SECRETS_FILE', default='./client_secrets.json')
OAUTH_OIDC_VALID_ISSUERS = config('OAUTH_OIDC_VALID_ISSUERS', default='https://')
OAUTH_OIDC_INTROSPECTION_AUTH_METHOD = config('OAUTH_OIDC_INTROSPECTION_AUTH_METHOD', default='client_secret_post')
OAUTH_OIDC_SCOPES = config('OAUTH_OIDC_SCOPES', default='openid,email,roles').split(",")
OAUTH_OIDC_CLOCK_SKEW = config('OAUTH_OIDC_CLOCK_SKEW', default=560, cast=int)
OAUTH_OIDC_ID_TOKEN_COOKIE_SECURE = config('OAUTH_SECRET_KEY', default='False', cast=bool)

UPLOAD_FOLDER = config('ROOT_UPLOAD_FOLDER',default="D:\\data\\")
ALLOWED_EXTENSIONS = config('ALLOWED_EXTENSIONS',default=['txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv', 'xls', 'xlsx', 'doc', 'docx'])