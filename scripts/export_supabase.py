"""
Database exporter script for Supabase PostgreSQL (LinguistAI).
Dumps DDL schema, tables, constraints, indexes, RLS policies, and all table data into a clean SQL file.
"""

import os
import sys
import json
import datetime
from decimal import Decimal
import django
from django.db import connection

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguistai_project.settings')
django.setup()

def sql_quote_literal(val):
    if val is None:
        return 'NULL'
    if isinstance(val, bool):
        return 'TRUE' if val else 'FALSE'
    if isinstance(val, (int, float, Decimal)):
        return str(val)
    if isinstance(val, (datetime.datetime, datetime.date, datetime.time)):
        return f"'{val.isoformat()}'"
    if isinstance(val, (dict, list)):
        escaped_json = json.dumps(val, ensure_ascii=False).replace("'", "''")
        return f"'{escaped_json}'::jsonb"
    
    val_str = str(val).replace("'", "''")
    return f"'{val_str}'"

def export_database(app_only=False):
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'exports')
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, "supabase_backup.sql")
    
    # Core app tables vs full database
    if app_only:
        table_order = [
            'users',
            'scenarios',
            'learning_sessions',
            'interaction_logs',
            'vocabulary_cards',
        ]
    else:
        table_order = [
            'django_migrations',
            'django_content_type',
            'auth_permission',
            'auth_group',
            'auth_group_permissions',
            'auth_user',
            'auth_user_groups',
            'auth_user_user_permissions',
            'django_admin_log',
            'django_session',
            'users',
            'scenarios',
            'learning_sessions',
            'interaction_logs',
            'vocabulary_cards',
        ]

    with connection.cursor() as cursor:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("-- =============================================================================\n")
            f.write(f"-- LinguistAI Supabase Database Backup\n")
            f.write(f"-- Exported on: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
            f.write("-- Database: PostgreSQL (Supabase)\n")
            f.write("-- =============================================================================\n\n")
            f.write("SET statement_timeout = 0;\n")
            f.write("SET lock_timeout = 0;\n")
            f.write("SET client_encoding = 'UTF8';\n")
            f.write("SET standard_conforming_strings = on;\n")
            f.write("SET check_function_bodies = false;\n")
            f.write("SET client_min_messages = warning;\n")
            f.write("SET row_security = off;\n\n")

            import shutil

            # 1. Sequences
            f.write("-- -----------------------------------------------------------------------------\n")
            f.write("-- SEQUENCES\n")
            f.write("-- -----------------------------------------------------------------------------\n")
            cursor.execute("""
                SELECT c.relname 
                FROM pg_class c 
                JOIN pg_namespace n ON n.oid = c.relnamespace 
                WHERE c.relkind = 'S' AND n.nspname = 'public'
                ORDER BY c.relname;
            """)
            all_sequences = [row[0] for row in cursor.fetchall()]
            if app_only:
                sequences = [s for s in all_sequences if 'scenarios' in s]
            else:
                sequences = all_sequences

            for seq in sequences:
                f.write(f'CREATE SEQUENCE IF NOT EXISTS public."{seq}";\n')
            f.write("\n")

            # 2. Table Schemas (DDL)
            f.write("-- -----------------------------------------------------------------------------\n")
            f.write("-- TABLE SCHEMAS (DDL)\n")
            f.write("-- -----------------------------------------------------------------------------\n")
            for table in table_order:
                # Check if table exists
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables 
                        WHERE table_schema = 'public' AND table_name = %s
                    );
                """, [table])
                if not cursor.fetchone()[0]:
                    continue

                cursor.execute("""
                    SELECT column_name, udt_name, is_nullable, column_default, character_maximum_length
                    FROM information_schema.columns 
                    WHERE table_schema = 'public' AND table_name = %s
                    ORDER BY ordinal_position;
                """, [table])
                columns = cursor.fetchall()

                col_defs = []
                for col in columns:
                    name, udt, is_null, default, max_len = col
                    type_str = udt.upper()
                    if udt == 'varchar':
                        type_str = f"VARCHAR({max_len})" if max_len else "VARCHAR(255)"
                    elif udt == 'text':
                        type_str = "TEXT"
                    elif udt == 'int4':
                        type_str = "INTEGER"
                    elif udt == 'int8':
                        type_str = "BIGINT"
                    elif udt == 'int2':
                        type_str = "SMALLINT"
                    elif udt == 'bool':
                        type_str = "BOOLEAN"
                    elif udt == 'timestamptz':
                        type_str = "TIMESTAMP WITH TIME ZONE"
                    elif udt == 'timestamp':
                        type_str = "TIMESTAMP"
                    elif udt == 'numeric':
                        type_str = "NUMERIC"
                    elif udt == 'float8':
                        type_str = "DOUBLE PRECISION"
                    elif udt == 'uuid':
                        type_str = "UUID"
                    elif udt == 'jsonb':
                        type_str = "JSONB"
                    elif udt == 'date':
                        type_str = "DATE"

                    null_str = "NOT NULL" if is_null == 'NO' else "NULL"
                    def_str = f" DEFAULT {default}" if default else ""
                    col_defs.append(f'    "{name}" {type_str} {null_str}{def_str}')

                # Constraints (PK, Unique)
                cursor.execute("""
                    SELECT conname, pg_get_constraintdef(oid) 
                    FROM pg_constraint 
                    WHERE conrelid = %s::regclass AND contype IN ('p', 'u')
                    ORDER BY contype DESC;
                """, [f'public."{table}"'])
                constraints = cursor.fetchall()
                for con_name, con_def in constraints:
                    col_defs.append(f'    CONSTRAINT "{con_name}" {con_def}')

                f.write(f'CREATE TABLE IF NOT EXISTS public."{table}" (\n')
                f.write(',\n'.join(col_defs))
                f.write('\n);\n\n')

            # 3. Foreign Key Constraints
            f.write("-- -----------------------------------------------------------------------------\n")
            f.write("-- FOREIGN KEY CONSTRAINTS\n")
            f.write("-- -----------------------------------------------------------------------------\n")
            for table in table_order:
                cursor.execute("""
                    SELECT conname, pg_get_constraintdef(oid) 
                    FROM pg_constraint 
                    WHERE conrelid = %s::regclass AND contype = 'f'
                    ORDER BY conname;
                """, [f'public."{table}"'])
                fks = cursor.fetchall()
                for con_name, con_def in fks:
                    f.write(f'ALTER TABLE public."{table}" DROP CONSTRAINT IF EXISTS "{con_name}";\n')
                    f.write(f'ALTER TABLE public."{table}" ADD CONSTRAINT "{con_name}" {con_def};\n')
            f.write("\n")

            # 4. Indexes
            f.write("-- -----------------------------------------------------------------------------\n")
            f.write("-- INDEXES\n")
            f.write("-- -----------------------------------------------------------------------------\n")
            format_tables = ", ".join([f"'{t}'" for t in table_order])
            cursor.execute(f"""
                SELECT indexdef 
                FROM pg_indexes 
                WHERE schemaname = 'public' 
                AND tablename IN ({format_tables})
                AND indexname NOT LIKE '%_pkey'
                ORDER BY tablename, indexname;
            """)
            indexes = cursor.fetchall()
            for idx in indexes:
                idx_def = idx[0]
                if not idx_def.endswith(';'):
                    idx_def += ';'
                f.write(f"{idx_def}\n")
            f.write("\n")

            # 5. Data (DML)
            f.write("-- -----------------------------------------------------------------------------\n")
            f.write("-- TABLE DATA (DML)\n")
            f.write("-- -----------------------------------------------------------------------------\n")
            total_records = 0
            for table in table_order:
                cursor.execute(f'SELECT * FROM public."{table}";')
                rows = cursor.fetchall()
                cols = [desc[0] for desc in cursor.description]
                col_list_str = ', '.join([f'"{c}"' for c in cols])

                f.write(f'-- Data for table: public."{table}" ({len(rows)} rows)\n')
                if rows:
                    for row in rows:
                        val_strs = [sql_quote_literal(v) for v in row]
                        f.write(f'INSERT INTO public."{table}" ({col_list_str}) VALUES ({", ".join(val_strs)});\n')
                    total_records += len(rows)
                f.write("\n")

            # 6. Sequence Updates
            f.write("-- -----------------------------------------------------------------------------\n")
            f.write("-- SEQUENCE CURRENT VALUES\n")
            f.write("-- -----------------------------------------------------------------------------\n")
            for seq in sequences:
                cursor.execute(f"SELECT last_value, is_called FROM public.\"{seq}\";")
                res = cursor.fetchone()
                if res:
                    last_val, is_called = res
                    f.write(f"SELECT setval('public.\"{seq}\"', {last_val}, {'true' if is_called else 'false'});\n")
            f.write("\n")

            # 7. RLS Policies
            f.write("-- -----------------------------------------------------------------------------\n")
            f.write("-- ROW LEVEL SECURITY & POLICIES\n")
            f.write("-- -----------------------------------------------------------------------------\n")
            cursor.execute(f"""
                SELECT tablename, rowsecurity 
                FROM pg_tables 
                WHERE schemaname = 'public'
                AND tablename IN ({format_tables});
            """)
            for t_name, rls in cursor.fetchall():
                if rls:
                    f.write(f'ALTER TABLE public."{t_name}" ENABLE ROW LEVEL SECURITY;\n')

            cursor.execute(f"""
                SELECT 
                    tablename, 
                    policyname, 
                    permissive, 
                    roles, 
                    cmd, 
                    qual, 
                    with_check 
                FROM pg_policies 
                WHERE schemaname = 'public'
                AND tablename IN ({format_tables})
                ORDER BY tablename, policyname;
            """)
            policies = cursor.fetchall()
            for pol in policies:
                t_name, p_name, permissive, roles, cmd, qual, with_check = pol
                f.write(f'DROP POLICY IF EXISTS "{p_name}" ON public."{t_name}";\n')
                roles_str = ', '.join(roles) if roles else 'PUBLIC'
                pol_sql = f'CREATE POLICY "{p_name}" ON public."{t_name}" FOR {cmd} TO {roles_str}'
                if qual:
                    pol_sql += f' USING ({qual})'
                if with_check:
                    pol_sql += f' WITH CHECK ({with_check})'
                pol_sql += ';\n'
                f.write(pol_sql)

    mode_desc = "Core app tables only (excluding Django internal tables)" if app_only else "Full database"
    print(f"Export [{mode_desc}] completed successfully!")
    print(f"File: {filepath}")
    print(f"Total records exported: {total_records}")
    return filepath

if __name__ == '__main__':
    args = sys.argv[1:]
    is_full = '--full' in args
    export_database(app_only=not is_full)
