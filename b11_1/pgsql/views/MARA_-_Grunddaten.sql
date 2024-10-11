DROP VIEW IF EXISTS MARA_Grunddaten;
CREATE VIEW MARA_Grunddaten AS
SELECT
    a.positions_nr AS SOURCE_ID,
    b.text AS MTART,
    c.text AS MEINS,
    a.herstellerteilenummer AS MFRPN,
    a.hersteller_nr_gp AS MFRNR,
    a.groesse_abmessung AS GROES,
    a.nettogewicht AS NTGEW,
    a.laenge AS LAENG,
    a.breite AS BREIT,
    a.hoehe AS HOEHE,
    'MM' AS MEABM,
    'KG' AS GEWEI,
    d.text AS PROFL,
    a.nato_versorgungs_nr AS NSNID,
    a.ean_upc_code AS EAN11,
    CASE WHEN a.ean_upc_code is null THEN '' ELSE 'HE' END AS NUMTP,
    e.text AS BEGRU,
    a.normbezeichnung AS NORMT,
    'M' AS MBRSH,
    a.warengruppe AS MATKL,
    '' AS BISMT,
    a.bruttogewicht AS BRGEW,
    a.bestellmengeneinheit AS BSTME,
    f.text AS SPART,
    CASE WHEN a.chargenpflicht = 'f' then 'N' else 'X' END AS XCHPF,
    'V1' AS MSTAE,
    '' AS MTPOS_MARA,
    CASE WHEN a.chargenpflicht = 'f' THEN '1' ELSE '2' END AS MCOND,
    a.fuehrendes_material AS ZZFUEHR_MAT,
    g.text AS ZZLABEL,
    h.text AS RETDELC,
    i.text AS ADSPC_SPC,
    a.produkthierarchie AS PRDHA,
    'UAM' AS HNDLCODE,
    j.text AS TEMPB,
    k.text AS ZZSONDERABLAUF,
    a.lagerfaehigkeit AS "MARA-MHDHB",
    '1' as "MARA-MHDRZ",
    '2' as "MARA-IPRKZ"
FROM b11_1_material a
left join b11_1_materialart b on b.id = a.materialart_grunddaten_id
left join b11_1_basismengeneinheit c on c.id = a.basismengeneinheit_id
left join b11_1_gefahrgutkennzeichen d on d.id = a.gefahrgutkennzeichen_id
left join b11_1_begru e on e.id = a.begru_id
left join b11_1_sparte f on f.id = a.sparte_id
left join b11_1_auszeichnungsfeld g on g.id = a.auszeichnungsfeld_id
left join b11_1_rueckfuehrungscode h on h.id = a.rueckfuehrungscode_id
left join b11_1_sparepartclasscode i on i.id = a.spare_part_class_code_id
left join b11_1_temperaturbedingung j on j.id = a.temperaturbedingung_id
left join b11_1_sonderablauf k on k.id = a.sonderablauf_id
where a.is_transferred='t';
