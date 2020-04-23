-- TPC-H/TPC-R Shipping Modes and Order Priority Query (Q12)
select
       l_shipmode,
       sum(case
           when o_orderpriority ='1-URGENT'
           or o_orderpriority ='2-HIGH'
           then 1
           else 0
       end) as high_line_count,
       sum(case
           when o_orderpriority <> '1-URGENT'
           and o_orderpriority <> '2-HIGH'
           then 1
           else 0
       end) as low_line_count
 from
      orders,
      lineitem
where
      o_orderkey = l_orderkey
  and l_shipmode in ('{SHIPMODE1}', '{SHIPMODE2}')
  and l_commitdate < l_receiptdate
  and l_shipdate < l_commitdate
  and l_receiptdate >= to_date('{DATE}')
  and l_receiptdate < dateadd(year, 1, to_date('{DATE}'))
group by
      l_shipmode
order by
      l_shipmode;