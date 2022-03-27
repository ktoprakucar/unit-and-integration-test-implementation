class PostgresClientConfig:

    def __init__(self,
                 url: str,
                 port: str,
                 database: str,
                 user_name: str,
                 password: str):
        self.url = url
        self.port = port
        self.database = database
        self.user_name = user_name
        self.password = password
