
class MigrationConfig(object):

    def __init__(self, db_name, db_user, db_password, db_host, db_port, db_type, sql_directory="db_migration", base_line=0):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_type = db_type
        self.sql_directory = sql_directory
        self.base_line = base_line
