from mkpipe.functions_spark import BaseLoader 

class PostgresLoader(BaseLoader):
    def __init__(self, config, settings):
        super().__init__(
            config,
            settings,
            driver_name='postgresql',
            driver_jdbc='org.postgresql.Driver',
        )

    def build_jdbc_url(self):
        return f'jdbc:{self.driver_name}://{self.host}:{self.port}/{self.database}?user={self.username}&password={self.password}&currentSchema={self.schema}'
