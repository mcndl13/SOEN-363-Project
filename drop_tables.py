from db_config import get_connection

SQL_DROP_TABLES = """
DO $$ DECLARE
    r RECORD;
BEGIN
    -- Drop all foreign key constraints first to avoid dependency issues
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'ALTER TABLE IF EXISTS ' || quote_ident(r.tablename) || ' DROP CONSTRAINT IF EXISTS ' || r.tablename || '_fkey';
    END LOOP;

    -- Drop all tables in the 'public' schema
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;

    -- Drop ENUM types
    FOR r IN (SELECT n.nspname as schema, t.typname as name
              FROM pg_type t
                   LEFT JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
              WHERE t.typtype = 'e') LOOP
        EXECUTE 'DROP TYPE IF EXISTS ' || quote_ident(r.name) || ' CASCADE';
    END LOOP;

    -- Drop DOMAIN types
    FOR r IN (SELECT domain_name FROM information_schema.domains WHERE domain_schema = 'public') LOOP
        EXECUTE 'DROP DOMAIN IF EXISTS ' || quote_ident(r.domain_name) || ' CASCADE';
    END LOOP;
END $$;
"""

def drop_all_tables():
    conn = get_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    cur = conn.cursor()

    try:
        cur.execute(SQL_DROP_TABLES)
        conn.commit()
        print("All tables, ENUM types, and DOMAIN types dropped successfully!")
    except Exception as e:
        print(f"Error while dropping tables: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    drop_all_tables()
