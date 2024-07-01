-- Drop the view if it already exists to avoid conflicts
DROP VIEW IF EXISTS MAKT_Beschreibung;

-- Create the view
CREATE VIEW MAKT_Beschreibung AS
-- Select German text and label it with 'D'
SELECT 
  positions_nr AS source_id, 
  'D' AS spras, 
  kurztext_de AS maktx
FROM b11_1_material

UNION ALL

-- Select French text and label it with 'F'
SELECT 
  positions_nr AS source_id, 
  'F' AS spras, 
  kurztext_fr AS maktx
FROM b11_1_material

UNION ALL

-- Select English text and label it with 'E'
SELECT 
  positions_nr AS source_id, 
  'E' AS spras, 
  kurztext_en AS maktx
FROM b11_1_material;

-- After creating the view, you can query it as a regular table
-- For example: SELECT * FROM MAKT_Beschreibung;

