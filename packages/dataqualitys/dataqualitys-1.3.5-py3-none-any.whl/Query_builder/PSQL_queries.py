from textwrap import dedent


class QueryBuilder:
    @staticmethod
    def null_check_query(database, schema, table, column):
        return f"""
            SELECT ROUND((COUNT(CASE WHEN {column} IS NULL THEN 1 END) * 100.0) / NULLIF(COUNT(*), 0),
            2) AS null_pct FROM {database}.{schema}.{table}
        """
    
    @staticmethod
    def pii_check_query(database, schema, table, column):
        return f"""SELECT {column} FROM {database}.{schema}.{table} LIMIT 1000"""
    
    @staticmethod
    def row_count_check_query(database, schema, table):
        return f"""SELECT count(*) as row_cnt FROM {database}.{schema}.{table} """

    @staticmethod
    def insert_audit_logs_query():
        return dedent("""
               INSERT INTO dq_audit.audit_results (
                   check_name, database, schema_name, table_name, column_name,
                   pii_type, matches, check_status, alert_status,
                   checked_at, run_id, alert_sent, alerted_via, alert_recipient
               ) VALUES (
                   :check_name, :database, :schema_name, :table_name, :column_name,
                   :pii_type, :matches, :check_status, :alert_status,
                   :checked_at, :run_id, :alert_sent, :alerted_via, :alert_recipient
               )
           """)

    @staticmethod
    def insert_profiling_results_query():
        return dedent("""
            INSERT INTO dq_audit.audit_profiling (
                run_id, database_name, profiled_at, schema_name, table_name,
                column_name, data_type, nullable, non_null_count,
                null_count, stats
            )
            VALUES (
                :run_id, :database_name, :profiled_at, :schema_name, :table_name,
                :column_name, :data_type, :nullable, :non_null_count,
                :null_count, :stats
            );
        """)
    @staticmethod
    def insert_check_results_query():
        return dedent("""
            INSERT INTO dq_audit.audit_checks (
               run_id, check_name, checked_at, database_name, schema_name,
              table_name, column_name, check_status, alert_status, alert_sent,
              alert_channel, alert_recipient, check_metadata
           )
           VALUES (
              :run_id, :check_name, :checked_at, :database_name, :schema_name,
              :table_name, :column_name, :check_status, :alert_status, :alert_sent,
              :alert_channel, :alert_recipient, :check_metadata
           );
        """)
    @staticmethod
    def create_profiling_result_table():
        return dedent("""
     CREATE SCHEMA IF NOT EXISTS dq_audit;
     CREATE SEQUENCE IF NOT EXISTS dq_audit.audit_profiling_profiling_id_seq;
     CREATE TABLE IF NOT EXISTS dq_audit.audit_profiling (
         profiling_id bigint NOT NULL DEFAULT nextval('dq_audit.audit_profiling_profiling_id_seq'::regclass),
         run_id uuid NOT NULL,
         profiled_at timestamp with time zone NOT NULL,
         database_name text COLLATE pg_catalog."default" NOT NULL,
         schema_name text COLLATE pg_catalog."default" NOT NULL,
         table_name text COLLATE pg_catalog."default" NOT NULL,
         column_name text COLLATE pg_catalog."default" NOT NULL,
         data_type text COLLATE pg_catalog."default" NOT NULL,
         nullable boolean NOT NULL,
         non_null_count bigint NOT NULL,
         null_count bigint NOT NULL,
         stats jsonb NOT NULL,
         CONSTRAINT audit_profiling_pkey PRIMARY KEY (profiling_id),
         CONSTRAINT audit_profiling_run_id_schema_name_table_name_column_name_key UNIQUE (run_id, schema_name, table_name, column_name)
     );
     CREATE INDEX IF NOT EXISTS idx_audit_profiling_stats
         ON dq_audit.audit_profiling USING gin (stats);

     CREATE INDEX IF NOT EXISTS idx_audit_profiling_table_col
         ON dq_audit.audit_profiling USING btree
         (schema_name COLLATE pg_catalog."default" ASC NULLS LAST,
          table_name COLLATE pg_catalog."default" ASC NULLS LAST,
          column_name COLLATE pg_catalog."default" ASC NULLS LAST);
     
""")
    @staticmethod
    def create_check_result_table():
        return dedent("""
        CREATE SCHEMA IF NOT EXISTS dq_audit;
        CREATE SEQUENCE IF NOT EXISTS dq_audit.audit_checks_check_id_seq;
        CREATE TABLE IF NOT EXISTS dq_audit.audit_checks (
        check_id bigint NOT NULL DEFAULT nextval('dq_audit.audit_checks_check_id_seq'::regclass),
        run_id uuid NOT NULL,
        check_name text COLLATE pg_catalog."default" NOT NULL,
        checked_at timestamp without time zone NOT NULL,
        database_name text COLLATE pg_catalog."default",
        schema_name text COLLATE pg_catalog."default",
        table_name text COLLATE pg_catalog."default",
        column_name text COLLATE pg_catalog."default",
        check_status text COLLATE pg_catalog."default" NOT NULL,
        alert_status boolean DEFAULT false,
        alert_sent boolean DEFAULT false,
        alert_channel text COLLATE pg_catalog."default",
        alert_recipient text COLLATE pg_catalog."default",
        check_metadata jsonb,
        CONSTRAINT audit_checks_pkey PRIMARY KEY (check_id),
        CONSTRAINT audit_checks_check_status_check CHECK (check_status = ANY (ARRAY['pass'::text, 'fail'::text, 'warn'::text]))
    );
    CREATE INDEX IF NOT EXISTS idx_audit_checks_metadata
        ON dq_audit.audit_checks USING gin (check_metadata);

    CREATE INDEX IF NOT EXISTS idx_audit_checks_table_col
        ON dq_audit.audit_checks USING btree
        (schema_name COLLATE pg_catalog."default" ASC NULLS LAST,
         table_name COLLATE pg_catalog."default" ASC NULLS LAST,
         column_name COLLATE pg_catalog."default" ASC NULLS LAST);
        """)

