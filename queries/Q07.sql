-- TPC-H/TPC-R Volume Shipping Query (Q7)
select
       supp_nation,
       cust_nation,
       l_year, sum(v1) as revenue
  from (
    select
           n1.n_name as supp_nation,
           n2.n_name as cust_nation,
           extract(year from l_shipdate::date) as l_year,
           l_extendedprice * (1 - l_discount) as v1
      from
           supplier,
           lineitem,
           orders,
           customer,
           nation n1,
           nation n2
     where
           s_suppkey = l_suppkey
       and o_orderkey = l_orderkey
       and c_custkey = o_custkey
       and s_nationkey = n1.n_nationkey
       and c_nationkey = n2.n_nationkey
       and (
              (n1.n_name = '{NATION1}' and n2.n_name = '{NATION2}')
           or (n1.n_name = '{NATION2}' and n2.n_name = '{NATION1}')
           )
       and l_shipdate between to_date('1995-01-01') and to_date('1996-12-31')
       ) shipping
 group by
       supp_nation,
       cust_nation,
       l_year
 order by
       supp_nation,
       cust_nation,
       l_year;