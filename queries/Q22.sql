-- TPC-H/TPC-R Global Sales Opportunity Query (Q22)
select
       cntrycode,
       count(*) as numcust,
       sum(acctbal) as totacctbal
  from (
    select
           substr(c_phone, 1, 2) as cntrycode,
           c_acctbal as acctbal -- hack: not actually in specification, we do this here because I am lazy!
      from
           customer
     where
           substr(c_phone, 1, 2) in ({CC1}, {CC2}, {CC3}, {CC4}, {CC5}, {CC6}, {CC7})
       and c_acctbal > (
            select
                   avg(c_acctbal)
              from
                   customer
             where
                   c_acctbal > 0.00
               and substr(c_phone, 1, 2) in ({CC1}, {CC2}, {CC3}, {CC4}, {CC5}, {CC6}, {CC7})
           )
       and not exists (
            select
                   *
              from
                   orders
             where
                   o_custkey = c_custkey
           )
       ) custsale
 group by
       cntrycode
 order by
       cntrycode;