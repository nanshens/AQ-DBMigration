# AQ-DBMigration
a db migration tool in python   

## install
`pip install aq-dbmigration`   

## how to use   

```python
    config = MigrationConfig("db_name", "db_user", "db_password", "db_host", "db_port", DBConstant.Type.PostgreSQL, "db file path")
    db = DBMigration(config)
    db.migration()
```

## sql file
file format: V{version}__{description}.sql   
example: V1__test.sql, V2__issue1.sql, V2.1__issue11.sql, V2.12__issue12.sql   

version:
version = main sequence + . + sub sequence, so order by main first, then sub.
example: V1.2 run first and V1.13 second, because 2 < 13.   

please start from V1

## MigrationConfig

### file path
please use absolute path.   
if you use flask, you can set db_path in flask config,
like this `app.config['DB_MIGRATION_PATH'] = os.path.join(app.root_path, 'resource', 'db_migration')`
and use `MigrationConfig("db_name", "db_user", "db_password", "db_host", "db_port", DBConstant.Type.PostgreSQL, app.config['DB_MIGRATION_PATH'])` to init   


### baseline
When used for the first time, it will set the baseline, and subsequent changes will not take effect.   
Only read sql files larger than baseline.   


## database support
1. postgresql(tested pass)
2. mysql(in testing)
3. maria(in testing)
4. sqlite(in testing)


## License
This project is licensed under the terms of the [GNU General Public License v3.0](LICENSE).
