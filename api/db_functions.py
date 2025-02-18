from django.db import connection

      
      
      
def fetch_received_energy(start_date, end_date, sub_code):
    query = """
      with jami as (
      select
        o.meter_no,
        obj_name,
        nominal,
        direction,
        qutb,
        dan.P0300 as dan_Ap,
        dan.P0400 as dan_Am,
        gacha.P0300 as gacha_Ap,
        gacha.P0400 as gacha_Am,
        case when gacha.P0300 is not null and dan.P0300 is not null 
        then (gacha.P0300 - dan.P0300) end as Ap_farq,
        case when gacha.P0400 is not null and dan.P0400 is not null 
        then (gacha.P0400 - dan.P0400) end as Am_farq,
        g.rate_current*g.rate_power as koef,
        case when gacha.P0300 is not null and dan.P0300 is not null 
        then (gacha.P0300 - dan.P0300) * g.rate_current*g.rate_power end as Ap_kwh,
        case when gacha.P0400 is not null and dan.P0400 is not null 
        then (gacha.P0400 - dan.P0400) * g.rate_current*g.rate_power end as Am_kwh
      from
        mes.map_sub_objects o
      left join mes.mes_general g on g.install_meter_no = o.meter_no 
      left join mes.mes_daily_cas dan on dan.meter_no = o.meter_no 
      and dan.freeze_date = to_date(%s, 'DD.MM.YYYY')
      left join mes.mes_daily_cas gacha on gacha.meter_no = o.meter_no
      and gacha.freeze_date = to_date(%s, 'DD.MM.YYYY')
      where
        o.belong_object_code = %s
        and o.obj_type not in ('sub', 'bus', 'tr')
      )
      select meter_no, obj_name, dan_Ap, gacha_Ap, Ap_farq, koef, Ap_kwh
      from jami
      where direction = 'in'
      union all
      select '===', null, null, null, null, null, null
      union all
      select meter_no, obj_name, dan_Am, gacha_Am, Am_farq, koef, Am_kwh
      from jami
      where direction = 'out';
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
      obj_name,
      nominal,
      direction,
      qutb,
      dan.P0300 as dan_Ap,
      dan.P0400 as dan_Am,
      gacha.P0300 as gacha_Ap,
      gacha.P0400 as gacha_Am,
      case when gacha.P0300 is not null and dan.P0300 is not null 
      then (gacha.P0300 - dan.P0300) end as Ap_farq,
      case when gacha.P0400 is not null and dan.P0400 is not null 
      then (gacha.P0400 - dan.P0400) end as Am_farq,
      g.rate_current*g.rate_power as koef,
      case when gacha.P0300 is not null and dan.P0300 is not null 
      then (gacha.P0300 - dan.P0300) * g.rate_current*g.rate_power end as Ap_kwh,
      case when gacha.P0400 is not null and dan.P0400 is not null 
      then (gacha.P0400 - dan.P0400) * g.rate_current*g.rate_power end as Am_kwh
    from
      mes.map_sub_objects o
    left join mes.mes_general g on g.install_meter_no = o.meter_no 
    left join mes.mes_daily_cas dan on dan.meter_no = o.meter_no 
    and dan.freeze_date = to_date(%s, 'DD.MM.YYYY')
    left join mes.mes_daily_cas gacha on gacha.meter_no = o.meter_no
    and gacha.freeze_date = to_date(%s, 'DD.MM.YYYY')
    where
      o.belong_object_code = %s
      and o.obj_type not in ('sub', 'bus', 'tr')
    )
    select meter_no, obj_name, dan_Am, gacha_Am, Am_farq, koef, Am_kwh
    from jami
    where direction = 'in'
    union all
    select '===', null, null, null, null, null, null
    union all
    select meter_no, obj_name, dan_Ap, gacha_Ap, Ap_farq, koef, Ap_kwh
    from jami
    where direction = 'out';
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date, sub_code])
        rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    return results




def fetch_object_by_code(obj_code):
    query = """
    SELECT * 
    FROM mes.map_sub_objects no2 
    WHERE no2.obj_code = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [obj_code])  # Pass obj_code as parameter
        row = cursor.fetchone()  # Fetch only the first row
    if row:
        columns = [col[0] for col in cursor.description]  # Get column names
        result = dict(zip(columns, row))  # Map column names to values in the row
        return result
    return None  # Return None if no matching row is found