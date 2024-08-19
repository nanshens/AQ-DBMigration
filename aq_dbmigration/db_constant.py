
class DBConstant:

    class Type:
        PostgreSQL = "PostgreSQL"
        MySql = "MySql"
        MariaDB = "MariaDB"
        SQLite = "SQLite"

    BASE_LINE = "<<DB BASE LINE>>"

    INIT_POSTGRESQL = f"""
        CREATE SCHEMA IF NOT EXISTS migration;
        create table if NOT EXISTS migration.aq_db_migration(
            id  character varying(50),
            sequence character varying(100),
            version character varying(100),
            description character varying(100),
            file_path character varying(100),
            install_time timestamp,
            execution_time int,
            check_value  character varying(100),
            CONSTRAINT aq_db_migration_pkey PRIMARY KEY (id)
        );
    """

    INIT_MYSQL = f"""
            CREATE TABLE IF NOT EXISTS aq_db_migration (
                id VARCHAR(50),
                sequence VARCHAR(100),
                version VARCHAR(100),
                description VARCHAR(100),
                file_path VARCHAR(100),
                install_time TIMESTAMP,
                execution_time INT,
                check_value VARCHAR(100),
                PRIMARY KEY (id)
            );
        """

    INIT_SQLITE = f"""
            CREATE TABLE IF NOT EXISTS aq_db_migration (
                id TEXT PRIMARY KEY,
                sequence TEXT,
                version TEXT,
                description TEXT,
                file_path TEXT,
                install_time TIMESTAMP,
                execution_time INTEGER,
                check_value TEXT
            );
        """

    @classmethod
    def get_init_sql(cls, type):
        if type == cls.Type.PostgreSQL:
            sql = cls.INIT_POSTGRESQL
        elif type in [cls.Type.MariaDB, cls.Type.MySql]:
            sql = cls.INIT_MYSQL
        elif type == cls.Type.SQLite:
            sql = cls.INIT_SQLITE
        else:
            sql = cls.INIT_POSTGRESQL
        return sql

    @classmethod
    def get_table_name(cls, type):
        if type == cls.Type.PostgreSQL:
            return 'migration.aq_db_migration'
        return 'aq_db_migration'