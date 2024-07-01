-- Create a view to transform the original result set into the desired normalized format
DROP VIEW IF EXISTS MARA_AUSP_Merkmale;
CREATE VIEW MARA_AUSP_Merkmale AS
WITH original_query AS (
    SELECT
        a.positions_nr AS source_id,
        '001' AS klart,
        a.a_nummer AS v_a_nummer,
        a.revision_fremd AS v_revfremd,
        a.revision_eigen AS v_reveigen,
        a.systemmanager AS v_systemmanager,
        b.text AS v_uebersetzung,
        a.kennziffer_bamf AS v_kennziffer,
        a.next_higher_assembly AS v_next_higher,
        -- Convert boolean fields to 'J' or '' based on their value
        CASE WHEN a.zertifiziert_fuer_flug = 't' THEN 'J' ELSE '' END AS v_zertflug,
        CASE WHEN a.verteilung_apm_kerda = 't' THEN 'X' ELSE '' END AS v_apm,
        CASE WHEN a.verteilung_cheops = 't' THEN 'X' ELSE '' END AS v_cheops,
        CASE WHEN a.verteilung_svsaa = 't' THEN 'X' ELSE '' END AS v_svsaa
    FROM b11_1_material a
    LEFT JOIN b11_1_uebersetzungsstatus b ON b.id = a.uebersetzungsstatus_id
    WHERE a.is_transferred = 't'
)
-- Generate the normalized format using UNION ALL for each field
SELECT
    source_id,
    klart,
    v_a_nummer AS atwrt,
    'V_A_NUMMER' AS atnam
FROM original_query
UNION ALL
SELECT
    source_id,
    klart,
    v_revfremd AS atwrt,
    'V_REVFREMD' AS atnam
FROM original_query
UNION ALL
SELECT
    source_id,
    klart,
    v_reveigen AS atwrt,
    'V_REVEIGEN' AS atnam
FROM original_query
UNION ALL
SELECT
    source_id,
    klart,
    v_systemmanager AS atwrt,
    'V_SYSTEMMANAGER' AS atnam
FROM original_query
UNION ALL
SELECT
    source_id,
    klart,
    v_uebersetzung AS atwrt,
    'V_UEBERSETZUNG' AS atnam
FROM original_query
UNION ALL
SELECT
    source_id,
    klart,
    v_kennziffer AS atwrt,
    'V_KENNZIFFER' AS atnam
FROM original_query
UNION ALL
SELECT
    source_id,
    klart,
    v_next_higher AS atwrt,
    'V_NEXT_HIGHER' AS atnam
FROM original_query
UNION ALL
SELECT
    source_id,
    klart,
    v_zertflug AS atwrt,
    'V_ZERTFLUG' AS atnam
FROM original_query
UNION ALL
SELECT
    source_id,
    klart,
    v_apm AS atwrt,
    'V_APM' AS atnam
FROM original_query
UNION ALL
SELECT
    source_id,
    klart,
    v_cheops AS atwrt,
    'V_CHEOPS' AS atnam
FROM original_query
UNION ALL
SELECT
    source_id,
    klart,
    v_svsaa AS atwrt,
    'V_SVSAA' AS atnam
FROM original_query
ORDER BY source_id, atnam;

-- Query the view to ensure it works as expected
--SELECT * FROM MARA_AUSP_Merkmale;

