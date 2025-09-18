from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text


async def setup_rls(engine: AsyncEngine) -> None:
    """Enable RLS and define tenant policies on multi-tenant tables.

    Assumes tables already exist. Policies are idempotent via IF NOT EXISTS.
    """
    tenant_tables = [
        "staff",
        "students",
        "parents",
        "parent_students",
        "classes",
        "courses",
        "class_teachers",
        "course_teachers",
        "enrollments",
        "academic_years",
        "terms",
    ]

    async with engine.begin() as conn:
        for table in tenant_tables:
            # Enable RLS
            await conn.execute(text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"))
            # SELECT policy
            await conn.execute(text(
                f"""
                DO $$ BEGIN
                  IF NOT EXISTS (
                    SELECT 1 FROM pg_policies WHERE schemaname = 'public' AND tablename = '{table}' AND policyname = 'rls_{table}_select'
                  ) THEN
                    EXECUTE 'CREATE POLICY rls_{table}_select ON {table} FOR SELECT USING (current_setting(''app.tenant_id'', true)::int = school_id)';
                  END IF;
                END $$;
                """
            ))
            # INSERT policy
            await conn.execute(text(
                f"""
                DO $$ BEGIN
                  IF NOT EXISTS (
                    SELECT 1 FROM pg_policies WHERE schemaname = 'public' AND tablename = '{table}' AND policyname = 'rls_{table}_insert'
                  ) THEN
                    EXECUTE 'CREATE POLICY rls_{table}_insert ON {table} FOR INSERT WITH CHECK (current_setting(''app.tenant_id'', true)::int = school_id)';
                  END IF;
                END $$;
                """
            ))
            # UPDATE policy
            await conn.execute(text(
                f"""
                DO $$ BEGIN
                  IF NOT EXISTS (
                    SELECT 1 FROM pg_policies WHERE schemaname = 'public' AND tablename = '{table}' AND policyname = 'rls_{table}_update'
                  ) THEN
                    EXECUTE 'CREATE POLICY rls_{table}_update ON {table} FOR UPDATE USING (current_setting(''app.tenant_id'', true)::int = school_id) WITH CHECK (current_setting(''app.tenant_id'', true)::int = school_id)';
                  END IF;
                END $$;
                """
            ))
