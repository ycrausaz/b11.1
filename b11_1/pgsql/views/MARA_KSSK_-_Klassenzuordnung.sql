-- Create a view named "MARA_KSSK_Klassenzuordnung"
DROP VIEW IF EXISTS MARA_KSSK_Klassenzuordnung;
CREATE VIEW MARA_KSSK_Klassenzuordnung AS
WITH source_data AS (
    SELECT a.positions_nr AS source_id,
           '001' AS klart
    FROM b11_1_material a
    WHERE a.is_transferred = 't'
)
SELECT source_id, 
       klart, 
       'V_VERTEILUNG_PSD' AS class
FROM source_data
UNION ALL
SELECT source_id, 
       klart, 
       'V_VERTEILUNG_RUAG' AS class
FROM source_data
UNION ALL
SELECT source_id, 
       klart, 
       'V_ZUSATZDATEN' AS class
FROM source_data
UNION ALL
SELECT source_id, 
       klart, 
       'V_AR_NUMMER' AS class
FROM source_data
UNION ALL
SELECT source_id, 
       klart, 
       'V_VERTEILUNG' AS class
FROM source_data
UNION ALL
SELECT source_id, 
       klart, 
       'V_BM_SBM' AS class
FROM source_data
ORDER BY source_id;

-- Now you can query the view just like a table
-- Example query to get all rows from the view
--SELECT * FROM MARA_KSSK_Klassenzuordnung;

