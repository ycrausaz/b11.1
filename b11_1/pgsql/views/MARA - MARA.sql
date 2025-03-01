CREATE OR REPLACE VIEW mara_mara
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    b.text AS mtart,
    c.text AS meins,
    a.herstellerteilenummer AS mfrpn,
    a.geschaeftspartner AS mfrnr,
    a.groesse_abmessung AS groes,
    a.nettogewicht AS ntgew,
    a.laenge AS laeng,
    a.breite AS breit,
    a.hoehe,
    'MM'::text AS meabm,
    'KG'::text AS gewei,
    d.text AS profl,
    a.nato_versorgungs_nr AS nsnid,
    a.ean_upc_code AS ean11,
        CASE
            WHEN a.ean_upc_code IS NULL THEN ''::text
            ELSE 'HE'::text
        END AS numtp,
    e.text AS begru,
    a.normbezeichnung AS normt,
    'M'::text AS mbrsh,
    a.warengruppe AS matkl,
    ''::text AS bismt,
    a.bruttogewicht AS brgew,
    a.bestellmengeneinheit AS bstme,
    f.text AS spart,
        CASE
            WHEN a.chargenpflicht = false THEN 'N'::text
            ELSE 'X'::text
        END AS xchpf,
    'V1'::text AS mstae,
    ''::text AS mtpos_mara,
        CASE
            WHEN a.chargenpflicht = false THEN '1'::text
            ELSE '2'::text
        END AS mcond,
    a.fuehrendes_material AS zzfuehr_mat,
    a.auszeichnungsfeld AS zzlabel,
    h.text AS retdelc,
    i.text AS adspc_spc,
    a.produkthierarchie AS prdha,
    'UAM'::text AS hndlcode,
    j.text AS tempb,
    k.text AS zzsonderablauf,
    '2'::text AS "IPRKZ",
    a.externe_warengruppe AS extwg,
        CASE
            WHEN a.kennzeichen_komplexes_system = true THEN 'X'::text
            ELSE ''::text
        END AS zzkomsys
   FROM b11_1_material a
     LEFT JOIN b11_1_materialart b ON b.idx = a.materialart_grunddaten_id
     LEFT JOIN b11_1_basismengeneinheit c ON c.idx = a.basismengeneinheit_id
     LEFT JOIN b11_1_gefahrgutkennzeichen d ON d.idx = a.gefahrgutkennzeichen_id
     LEFT JOIN b11_1_begru e ON e.idx = a.begru_id
     LEFT JOIN b11_1_sparte f ON f.idx = a.sparte_id
     LEFT JOIN b11_1_rueckfuehrungscode h ON h.idx = a.rueckfuehrungscode_id
     LEFT JOIN b11_1_sparepartclasscode i ON i.idx = a.spare_part_class_code_id
     LEFT JOIN b11_1_temperaturbedingung j ON j.idx = a.temperaturbedingung_id
     LEFT JOIN b11_1_sonderablauf k ON k.idx = a.sonderablauf_id
  WHERE a.is_transferred = true;
