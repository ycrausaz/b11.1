-- Create a view named 'unpivoted_werks_view' that unpivots werk columns into rows
DROP VIEW IF EXISTS CKMLCR_Material_Ledger_Preise;
CREATE VIEW  CKMLCR_Material_Ledger_Preise AS
WITH material_data AS (
    -- CTE to get data from b11_1_material and related tables
    SELECT 
        a.positions_nr AS source_id, 
        b.text AS werk_1, 
        c.text AS werk_2, 
        d.text AS werk_3, 
        e.text AS werk_4, 
        a.preis AS PVPRS,
        a.preis AS STPRS,
        a.preiseinheit AS PEINH,
        '10' AS CURTP,
        'CHF' AS WAERS,
        a.preissteuerung_id AS VPRSV
    FROM 
        b11_1_material a
    LEFT JOIN 
        b11_1_werk_1 b ON a.werk_1_id = b.id
    LEFT JOIN 
        b11_1_werk_2 c ON a.werk_2_id = c.id
    LEFT JOIN 
        b11_1_werk_3 d ON a.werk_3_id = d.id
    LEFT JOIN 
        b11_1_werk_4 e ON a.werk_4_id = e.id
    LEFT JOIN
        b11_1_bewertungsklasse f on a.bewertungsklasse_id = f.id
    WHERE is_transferred = 't'
)
-- Unpivot the werk columns into rows
SELECT 
    source_id, 
    werk AS BWKEY, 
    PVPRS,
    STPRS,
    PEINH,
    CURTP,
    WAERS,
    VPRSV
FROM (
    SELECT 
        source_id, 
        werk_1 AS werk, 
        PVPRS,
        STPRS,
        PEINH,
        CURTP,
        WAERS,
        VPRSV
        FROM 
        material_data
    UNION ALL
    SELECT 
        source_id, 
        werk_2 AS werk, 
        PVPRS,
        STPRS,
        PEINH,
        CURTP,
        WAERS,
        VPRSV
    FROM 
        material_data
    UNION ALL
    SELECT 
        source_id, 
        werk_3 AS werk, 
        PVPRS,
        STPRS,
        PEINH,
        CURTP,
        WAERS,
        VPRSV
    FROM 
        material_data
    UNION ALL
    SELECT 
        source_id, 
        werk_4 AS werk, 
        PVPRS,
        STPRS,
        PEINH,
        CURTP,
        WAERS,
        VPRSV
    FROM 
        material_data
) AS unpivoted_data
ORDER BY 
    source_id, 
    BWKEY;

