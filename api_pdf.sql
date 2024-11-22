
-------------------------------------------------------------------------
SELECT * FROM api_report;
INSERT INTO api_report(title,"content",created_at) VALUES ('test','test',now());


--TRUNCATE TABLE user_tokens;

SELECT * FROM user_tokens;

SELECT h.soato,
    h.meterno,
    h.customertype,
    h.accountid,
    c.customer_type AS cas_customer_type,
    c.account_id AS cas_account_id,
        CASE
            WHEN c.customer_type::text = h.customertype::text THEN 0
            ELSE 1
        END AS customer_type_xato,
        CASE
            WHEN c.account_id::text = h.accountid::text THEN 0
            ELSE 1
        END AS account_id_xato,
        CASE
            WHEN c.account_id IS  NULL THEN 1
            ELSE 0
        END AS casda_mavjud_emas,
    het_billing.is_askue(h.meterno) AS is_askue
   FROM het_billing.get_daily_table(het_billing.get_max_table_sana()) h(soato, customertype, accountid, meterno, lastpokdate, balancecustomer, relaystatus, meterstatus, consumer_status)
     LEFT JOIN het_billing.cas_all c ON   h.soato::TEXT = c.soato::text AND h.meterno::TEXT=c.meter_no::text   WHERE h.meterno='121207108824';

 
 
 SELECT
    b.soato
    , b.meterno
    , b.accountid
    , ca.account_id c_acc
    ,CASE WHEN ca.account_id IS NULL THEN 1 ELSE NULL END casda_mavjudmas
FROM
    het_billing_customers_21112024 b
LEFT JOIN cas_all ca ON
    ca.meter_no = b.meterno
    AND ca.soato = b.soato WHERE b.meterno ='121207108824';
    

