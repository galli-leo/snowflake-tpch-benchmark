-- TPC-H/TPC-R Parts/Supplier Relationship Query (Q16)
select
       p_brand,
       p_type,
       p_size,
       count(distinct ps_suppkey) as supplier_cnt
  from
       partsupp,
       part
 where
       p_partkey = ps_partkey
   and p_brand <> '{BRAND}'
   and p_type not like '{TYPE}%'
   and p_size in ({SIZE1}, {SIZE2}, {SIZE3}, {SIZE4}, {SIZE5}, {SIZE6}, {SIZE7}, {SIZE8})
   and ps_suppkey not in (
    select
           s_suppkey
      from
           supplier
     where
           s_comment like '%Customer%Complaints%'
       )
 group by
       p_brand,
       p_type,
       p_size
 order by
       4 desc,
       p_brand,
       p_type,
       p_size
 limit 20;