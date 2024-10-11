-- Drop the view if it already exists to avoid errors during creation
DROP VIEW IF EXISTS MARA_STXL_Grunddaten;

-- Create the new view with the required transformation
CREATE VIEW MARA_STXL_Grunddaten AS
SELECT 
    source_id,
    'MATERIAL' AS tdobject,
    source_id AS tdname,
    'GRUN' AS tdid,
    tdspras,
    line_counter,
    tdformat,
    text AS tdline
FROM (
    -- Select for German 1st line
    SELECT 
        positions_nr AS source_id,
        'D' AS tdspras,
        1 AS line_counter,
        '' AS tdformat,
        grunddatentext_de_1_zeile AS text
    FROM b11_1_material
    WHERE is_transferred = 't'

    UNION ALL

    -- Select for German 2nd line
    SELECT 
        positions_nr,
        'D',
        2,
        '/' AS tdformat,
        grunddatentext_de_2_zeile
    FROM b11_1_material
    WHERE is_transferred = 't'

    UNION ALL

    -- Select for French 1st line
    SELECT 
        positions_nr,
        'F',
        1,
        '' AS tdformat,
        grunddatentext_fr_1_zeile
    FROM b11_1_material
    WHERE is_transferred = 't'

    UNION ALL

    -- Select for French 2nd line
    SELECT 
        positions_nr,
        'F',
        2,
        '/' AS tdformat,
        grunddatentext_fr_2_zeile
    FROM b11_1_material
    WHERE is_transferred = 't'

    UNION ALL

    -- Select for English 1st line
    SELECT 
        positions_nr,
        'E',
        1,
        '' AS tdformat,
        grunddatentext_en_1_zeile
    FROM b11_1_material
    WHERE is_transferred = 't'

    UNION ALL

    -- Select for English 2nd line
    SELECT 
        positions_nr,
        'E',
        2,
        '/' AS tdformat,
        grunddatentext_en_2_zeile
    FROM b11_1_material
    WHERE is_transferred = 't'
) AS MARA_STXL_Grunddaten
ORDER BY source_id, tdspras, line_counter;

