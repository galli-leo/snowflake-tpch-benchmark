-- TPC-H/TPC-R Product Type Profit Measure Query (Q9)
select
       nation,
       o_year,
       sum(amount) as sum_profit
  from (
    select
           n_name as nation,
           extract(year from o_orderdate::date) as o_year,
           l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount
      from
           part,
           supplier,
           lineitem,
           partsupp,
           orders,
           nation
     where
           s_suppkey = l_suppkey
       and ps_suppkey = l_suppkey
       and ps_partkey = l_partkey
       and p_partkey = l_partkey
       and o_orderkey = l_orderkey
       and s_nationkey = n_nationkey
       and p_name like '%{COLOR}%'
       ) profit
 group by
       nation,
       o_year
 order by
       nation,
       o_year desc;