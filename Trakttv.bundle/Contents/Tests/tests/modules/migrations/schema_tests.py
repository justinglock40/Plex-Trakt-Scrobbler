from plugin.core.database import Database
from plugin.modules.migrations.schema import SchemaMigration
from tests.helpers.database import DatabaseContext


def test_database_fresh():
    db = Database._connect(':memory:', 'peewee')

    with DatabaseContext.use(db):
        m = SchemaMigration()

        # Run fresh schema migration
        assert m.run() is True


def test_database_upgrade():
    db = Database._connect(':memory:', 'peewee')

    with DatabaseContext.use(db):
        m = SchemaMigration()

        # Run initial migration
        router = m._build_router()
        router.run('000_initial')

        # Run schema migration
        assert m.run() is True


def test_database_corruption():
    db = Database._connect(':memory:', 'peewee')

    with DatabaseContext.use(db):
        m = SchemaMigration()

        # Run initial migration
        router = m._build_router()
        router.run('000_initial')

        # Remove table from database (schema corruption)
        db.execute_sql('DROP TABLE "configuration.option"')

        # Ensure migration validation fails
        assert router.validate() is False

        # Run schema migration
        assert m.run() is True
