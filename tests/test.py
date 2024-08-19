from aq_dbmigration.db_constant import DBConstant
from aq_dbmigration.db_migration import DBMigration
from aq_dbmigration.migration_config import MigrationConfig

if __name__ == '__main__':
    config = MigrationConfig("", "", "", "127.0.0.1", "5432", DBConstant.Type.PostgreSQL)
    db = DBMigration(config)
    db.migration()