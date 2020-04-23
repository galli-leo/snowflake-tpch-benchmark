-- TPC-H/TPC-R National Market Share Query (Q8)
select
       o_year,
       sum(case
           when nation = '{NATION}'
           then v1
           else 0
           end) / sum(v1) as mkt_share
  from (
    select
           extract(year from o_orderdate) as o_year,
           l_extendedprice * (1-l_discount) as v1,
           n2.n_name as nation
      from
           part,
           supplier,
           lineitem,
           orders,
           customer,
           nation n1,
           nation n2,
           region
     where
           p_partkey = l_partkey
       and s_suppkey = l_suppkey
       and l_orderkey = o_orderkey
       and o_custkey = c_custkey
       and c_nationkey = n1.n_nationkey
       and n1.n_regionkey = r_regionkey
       and r_name = '{REGION}'
       and s_nationkey = n2.n_nationkey
       and o_orderdate between to_date('1995-01-01') and to_date('1996-12-31')
       and p_type = '{TYPE}'
      ) all_nations
 group by
       o_year
 order by
       o_year;