DO $$ 
DECLARE 
    r RECORD;
BEGIN
    -- Disable all triggers
    EXECUTE 'SET session_replication_role = replica';
    
    -- Drop all tables in the current schema
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
    
    -- Re-enable all triggers
    EXECUTE 'SET session_replication_role = DEFAULT';
END $$;

-- DROP MATERIALIZED VIEW customercontract;
-- DROP MATERIALIZED VIEW lastinvoicedetailspercustomer;