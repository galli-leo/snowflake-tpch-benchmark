-- TPC-H/TPC-R Important Stock Identification Query (Q11)
select
       ps_partkey,
       sum(ps_supplycost * ps_availqty) as value
from
       partsupp,
       supplier,
       nation
where
       ps_suppkey = s_suppkey
  and s_nationkey = n_nationkey
  and n_name = '{NATION}'
group by
      ps_partkey
    having
      sum(ps_supplycost * ps_availqty) > (
    select
           sum(ps_supplycost * ps_availqty) * {FRACTION}
      from
           partsupp,
           supplier,
           nation
     where
           ps_suppkey = s_suppkey
       and s_nationkey = n_nationkey
       and n_name = '{NATION}'
     )
order by
      2 desc
limit 20;