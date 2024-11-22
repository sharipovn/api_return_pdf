from django.db import connection

      
      
      
def fetch_received_energy(start_date, end_date, sub_code):
    query = """
    WITH jami AS (
        SELECT
          o.meter_no,
          object_name,
          nominal,
          direction,
          qutb,
          dan.P0300 AS dan_Ap,
          dan.P0400 AS dan_Am,
          gacha.P0300 AS gacha_Ap,
          gacha.P0400 AS gacha_Am,
          CASE WHEN gacha.P0300 IS NOT NULL AND dan.P0300 IS NOT NULL 
          THEN (gacha.P0300 - dan.P0300) END AS Ap_farq,
          CASE WHEN gacha.P0400 IS NOT NULL AND dan.P0400 IS NOT NULL 
          THEN (gacha.P0400 - dan.P0400) END AS Am_farq,
          mes.toka(ct_ratio) * mes.toka(pt_ratio) AS koef,
          CASE WHEN gacha.P0300 IS NOT NULL AND dan.P0300 IS NOT NULL 
          THEN (gacha.P0300 - dan.P0300) * mes.toka(ct_ratio) * mes.toka(pt_ratio) END AS Ap_kwh,
          CASE WHEN gacha.P0400 IS NOT NULL AND dan.P0400 IS NOT NULL 
          THEN (gacha.P0400 - dan.P0400) * mes.toka(ct_ratio) * mes.toka(pt_ratio) END AS Am_kwh
        FROM
          mes.n_objects o
        LEFT JOIN mes.mes_daily_cas dan ON dan.meter_no = o.meter_no 
        AND dan.freeze_date = TO_DATE(%s, 'DD.MM.YYYY')
        LEFT JOIN mes.mes_daily_cas gacha ON gacha.meter_no = o.meter_no
        AND gacha.freeze_date = TO_DATE(%s, 'DD.MM.YYYY')
        WHERE
          o.belong_object_code = %s
          AND o.object_type NOT IN ('sub', 'bus', 'tr')
    )
    SELECT meter_no, object_name, dan_Ap, gacha_Ap, Ap_farq, koef, Ap_kwh
    FROM jami
    WHERE direction = 'in'
    UNION ALL
    SELECT '===', NULL, NULL, NULL, NULL, NULL, NULL
    UNION ALL
    SELECT meter_no, object_name, dan_Am, gacha_Am, Am_farq, koef, Am_kwh
    FROM jami
    WHERE direction = 'out';
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date, sub_code])
        rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    return results




def fetch_transmissed_energy(start_date, end_date, sub_code):
    query = """
    with jami as (
      select
        o.meter_no,
        object_name,
        nominal,
        direction,
        qutb,
        dan.P0300 as dan_Ap,
        dan.P0400 as dan_Am,
        gacha.P0300 as gacha_Ap,
        gacha.P0300 as gacha_Am,
        case when gacha.P0300 is not null and dan.P0300 is not null 
        then (gacha.P0300 - dan.P0300) end as Ap_farq,
        case when gacha.P0400 is not null and dan.P0400 is not null 
        then (gacha.P0400 - dan.P0400) end as Am_farq,
        mes.toka(ct_ratio)*mes.toka(pt_ratio) as koef,
        case when gacha.P0300 is not null and dan.P0300 is not null 
        then (gacha.P0300 - dan.P0300) * mes.toka(ct_ratio)*mes.toka(pt_ratio) end as Ap_kwh,
        case when gacha.P0400 is not null and dan.P0400 is not null 
        then (gacha.P0400 - dan.P0400) * mes.toka(ct_ratio)*mes.toka(pt_ratio) end as Am_kwh
      from
        mes.n_objects o
      left join mes.mes_daily_cas dan on dan.meter_no = o.meter_no 
      and dan.freeze_date = to_date(%s, 'DD.MM.YYYY')
      left join mes.mes_daily_cas gacha on gacha.meter_no = o.meter_no
      and gacha.freeze_date = to_date(%s, 'DD.MM.YYYY')
      where
        o.belong_object_code = %s
        and o.object_type not in ('sub', 'bus', 'tr')
      )
      select meter_no, object_name, dan_Am, gacha_Am, Am_farq, koef, Am_kwh
      from jami
      where direction = 'in'
      union all
      select '===', null, null, null, null, null, null
      union all
      select meter_no, object_name, dan_Ap, gacha_Ap, Ap_farq, koef, Ap_kwh
      from jami
      where direction = 'out';
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date, sub_code])
        rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    return results




def fetch_object_by_code(object_code):
    query = """
    SELECT * 
    FROM mes.n_objects no2 
    WHERE no2.object_code = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [object_code])  # Pass object_code as parameter
        row = cursor.fetchone()  # Fetch only the first row
    if row:
        columns = [col[0] for col in cursor.description]  # Get column names
        result = dict(zip(columns, row))  # Map column names to values in the row
        return result
    return None  # Return None if no matching row is found