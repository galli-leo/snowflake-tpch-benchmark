-- TPC-H/TPC-R Top Supplier Query (Q15)
with
  tpch_revenue as (
    select
      l_suppkey as supplier_no,
      sum(l_extendedprice * (1 - l_discount)) as total_revenue
    from
      lineitem
    where
      l_shipdate >= '{DATE}' and
      l_shipdate <  dateadd(month, 3, to_date('{DATE}'))
    group by l_suppkey
  )
select
      s_suppkey,
      s_name,
      s_address,
      s_phone,
      total_revenue
 from
      supplier,
      tpch_revenue
where
      s_suppkey = supplier_no
      and total_revenue = (
       select
              max(total_revenue)
         from
              tpch_revenue
      )
order by
      s_suppkey;