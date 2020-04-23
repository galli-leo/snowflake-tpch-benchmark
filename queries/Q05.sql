-- TPC-H/TPC-R Local Supplier Volume Query (Q5)
select
       n_name,
       sum(l_extendedprice * (1 - l_discount)) as revenue
  from
       customer,
       orders,
       lineitem,
       supplier,
       nation,
       region
 where
       c_custkey = o_custkey
   and l_orderkey = o_orderkey
   and l_suppkey = s_suppkey
   and c_nationkey = s_nationkey
   and s_nationkey = n_nationkey
   and n_regionkey = r_regionkey
   and r_name = '{REGION}'
   and o_orderdate >= to_date('{DATE}')
   and o_orderdate < dateadd(year, 1, to_date('{DATE}'))
 group by
       n_name
 order by
       2 desc;