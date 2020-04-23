-- TPC-H/TPC-R Shipping Priority Query (Q3)
select
       l_orderkey,
       sum(l_extendedprice*(1-l_discount)) as revenue,
       o_orderdate,
       o_shippriority
  from
       customer,
       orders,
       lineitem
where
       c_mktsegment = '{SEGMENT}'
   and c_custkey = o_custkey
   and l_orderkey = o_orderkey
   and o_orderdate < to_date('{DATE}')
   and l_shipdate > to_date('{DATE}')
 group by
       l_orderkey,
       o_orderdate,
       o_shippriority
 order by
       2 desc,
       o_orderdate
 limit 10;