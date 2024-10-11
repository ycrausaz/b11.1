-- Drop the view if it already exists to avoid conflicts
DROP VIEW IF EXISTS MARA_STXH_Grunddaten;

-- Create the view
CREATE VIEW MARA_STXH_Grunddaten AS
-- Select German text and label it with 'D'
SELECT 
  positions_nr AS source_id, 
  'MATERIAL' AS tdobject,
  positions_nr AS TDNAME,
  'GRUN' AS TDID,
  'D' AS TDSPRAS
FROM b11_1_material
WHERE is_transferred = 't'

UNION ALL

-- Select French text and label it with 'F'
SELECT 
  positions_nr AS source_id, 
  'MATERIAL' AS tdobject,
  positions_nr AS TDNAME,
  'GRUN' AS TDID,
  'F' AS TDSPRAS
FROM b11_1_material
WHERE is_transferred = 't'

UNION ALL

-- Select English text and label it with 'E'
SELECT 
  positions_nr AS source_id, 
  'MATERIAL' AS tdobject,
  positions_nr AS TDNAME,
  'GRUN' AS TDID,
  'E' AS TDSPRAS
FROM b11_1_material
WHERE is_transferred = 't'
ORDER BY source_id;

-- After creating the view, you can query it as a regular table
-- For example: SELECT * FROM MARA_STXH_Grunddaten;

