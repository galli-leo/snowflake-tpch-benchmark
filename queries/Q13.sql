-- TPC-H/TPC-R Customer Distribution Query (Q13)
select
       c_count,
       count(*) as custdist
  from (
    select
           c_custkey,
           count(o_orderkey) as c_count
      from
           customer
      left outer join
           orders
        on
           c_custkey = o_custkey
           and o_comment not like '%{WORD1}%{WORD2}%'
           group by
           c_custkey
       ) c_orders
 group by
       c_count
 order by
       2 desc,
       c_count desc;