DROP VIEW IF EXISTS MLAN_Steuer;
CREATE VIEW MLAN_Steuer AS
SELECT
    positions_nr AS SOURCE_ID,
    'CH' AS ALAND
FROM b11_1_material
where is_transferred='t';
