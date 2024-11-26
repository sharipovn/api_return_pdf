
-------------------------------------------------------------------------
SELECT * FROM api_report;
INSERT INTO api_report(title,"content",created_at) VALUES ('test','test',now());




SELECT soato,customertype,accountid,meternom FROM het_billing_customers_21112024 hbc WHERE meterno ='111220194983'


SELECT 
    'http://192.168.14.167:8000/api/generate-pdf/?token=' || md5(username||KEY||to_char(current_timestamp
, 'DD.MM.YYYY HH24:MI'))||'&sub=sub_00004&dan=01.10.2024&gacha=01.11.2024' AS url
FROM   ies.users_for_tkn;



SELECT to_char(current_timestamp
    , 'DD.MM.YYYY HH24:MI');
    

SELECT md5('22.11.2024 10:591nuriddin'); 



------------------------------------------------------------------accespt---------------------------
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
and dan.freeze_date = to_date('01.10.2024', 'DD.MM.YYYY')
left join mes.mes_daily_cas gacha on gacha.meter_no = o.meter_no
and gacha.freeze_date = to_date('01.11.2024', 'DD.MM.YYYY')
where
  o.belong_object_code = 'sub_00001'
  and o.object_type not in ('sub', 'bus', 'tr')
)
select meter_no, object_name, dan_Ap, gacha_Ap, Ap_farq, koef, Ap_kwh
from jami
where direction = 'in'
union all
select '===', null, null, null, null, null, null
union all
select meter_no, object_name, dan_Am, gacha_Am, Am_farq, koef, Am_kwh
from jami
where direction = 'out'
;


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
and dan.freeze_date = to_date('01.10.2024', 'DD.MM.YYYY')
left join mes.mes_daily_cas gacha on gacha.meter_no = o.meter_no
and gacha.freeze_date = to_date('01.11.2024', 'DD.MM.YYYY')
where
  o.belong_object_code = 'sub_00001'
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
where direction = 'out'
;


SELECT * FROM mes.n_objects no2 WHERE no2.object_code ='sub_00014';