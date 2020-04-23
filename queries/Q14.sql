-- TPC-H/TPC-R Promotion Effect Query (Q14)
select
       100.00 * sum(case
       when p_type like 'PROMO%'
       then l_extendedprice*(1-l_discount)
       else 0
       end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
  from
       lineitem,
       part
 where l_partkey = p_partkey
   and l_shipdate >= to_date('{DATE}')
   and l_shipdate < dateadd(month, 1, to_date('{DATE}'));