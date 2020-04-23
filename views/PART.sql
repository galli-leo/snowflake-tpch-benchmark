select
        src:P_PARTKEY as P_PARTKEY,
	src:P_NAME as P_NAME,
	src:P_MFGR as P_MFGR,
	src:P_BRAND as P_BRAND,
	src:P_TYPE as P_TYPE,
	src:P_SIZE as P_SIZE,
	src:P_CONTAINER as P_CONTAINER,
	src:P_RETAILPRICE as P_RETAILPRICE,
	src:P_COMMENT as P_COMMENT
    from PART_RAW