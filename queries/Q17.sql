-- TPC-H/TPC-R Small-Quantity-Order Revenue Query (Q17)
select
       sum(l_extendedprice) / 7.0 as avg_yearly
  from
       lineitem,
       part
 where
       p_partkey = l_partkey
   and p_brand = '{BRAND}'
   and p_container = '{CONTAINER}'
   and l_quantity < (
    select
           0.2 * avg(l_quantity)
      from
           lineitem
     where
           l_partkey = p_partkey
      );