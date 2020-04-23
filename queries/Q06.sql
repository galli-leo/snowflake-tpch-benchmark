-- TPC-H/TPC-R Forecasting Revenue Change Query (Q6)
select
       sum(l_extendedprice*l_discount) as revenue
  from
       lineitem
 where
       l_shipdate >= to_date('{DATE}')
   and l_shipdate < dateadd(year, 1, to_date('{DATE}'))
   and l_discount >= {DISCOUNT} - 0.01 and l_discount <= {DISCOUNT} + 0.01
   and l_quantity < {QUANTITY};