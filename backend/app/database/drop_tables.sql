-- INSTRUCTIONS
-- Open PgAdmin4, right click on tables 
-- Click onQuery Tool 
-- copy paste this in and execute to drop all tables

DO $$ 
DECLARE 
    r RECORD; 
BEGIN 
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') 
    LOOP 
        EXECUTE 'DROP TABLE IF EXISTS ' || r.tablename || ' CASCADE'; 
    END LOOP; 
END $$;