import logging
import random
import os
import log
import pandas as pd
import itertools
from extract_schema import get_tables

logger = logging.getLogger("query")

nations = {}
with open("nations.csv") as f:
    f.readline() # skip header
    for line in f.readlines():
        if line.strip() != "":
            name, region = line.split(",")
            region = int(region)
            nations[name] = region

regions = ["AFRICA", "AMERICA", "ASIA", "EUROPE", "MIDDLE EAST"]
types = [
    ["STANDARD", "SMALL", "MEDIUM", "LARGE", "ECONOMY", "PRO"], # syllable 1
    ["ANODIZED", "BURNISHED", "PLATED", "POLISHED", "BRUSHED"], # syllable 2
    ["TIN", "NICKEL", "BRASS", "STEEL", "COPPER"] # syllable 3
]
containers = [
    ["SM", "LG", "MED", "JUMBO", "WRAP"], # syllable 1
    ["CASE", "BOX", "BAG", "JAR", "PKG", "PACK", "CAN", "DRUM"] # syllable 2
]
tables = get_tables()

class query:
    def __init__(self, filename):
        self.filename = filename
        name = os.path.splitext(os.path.basename(self.filename))[0]
        self.num = int(name[1:])
        self.logger = logging.getLogger(name)
        self.sf = 100
        self.load()

    def load(self):
        self.logger.info("Loading query from %s", self.filename)
        self.contents = None
        with open(self.filename) as f:
            self.contents = f.read()
        self.desc = self.contents.split("\n")[0]
        self.desc = self.desc.replace("-- ", "")
        self.logger.info("Query description: %s", self.desc)
        self.build_args()

    def get_sql(self, schemaless=False):
        sql = self.contents.format([], **self.args)
        if schemaless:
            for tbl, carr in tables.items():
                raw_name = "src"
                for column, type in carr:
                    sql = sql.replace(column.lower(), f"{tbl.lower()}.{raw_name}:{column.upper()}::{type}")
        sql = sql.replace("n1.nation.src", "n1.src")
        sql = sql.replace("n2.nation.src", "n2.src")
        sql = sql.replace("l1.lineitem.src", "l1.src")
        sql = sql.replace("l2.lineitem.src", "l2.src")
        sql = sql.replace("l3.lineitem.src", "l3.src")

        return sql

    def random_choice_prod(self, *args):
        choice = random.choice(list(itertools.product(*args)))
        return " ".join(choice)

    def add_arg(self, name, fn, additional_fn = None):
        name = name.upper()
        self.args[name] = fn()
        rep_count = 0
        distinct = False
        if additional_fn is not None:
            distinct, rep_count = additional_fn()
        arr = []
        for i in range(rep_count):
            val = fn()
            if distinct:
                while val in arr:
                    val = fn(i)
            arr.append(val)
        for i, val in enumerate(arr):
            self.args[f"{name}{i+1}"] = val

    def build_args(self):
        self.args = {}
        self.add_arg("delta", self.get_delta)
        self.add_arg("size", self.get_size, self.additional_size)
        self.add_arg("type", self.get_type)
        self.add_arg("nation", self.get_nation, self.additional_nation)
        self.add_arg("region", self.get_region)
        self.add_arg("segment", self.get_segment)
        self.add_arg("date", self.get_date)
        self.add_arg("discount", self.get_discount)
        self.add_arg("quantity", self.get_quantity, self.additional_quantity) # todo fix query 19
        self.add_arg("color", self.get_color)
        self.add_arg("fraction", self.get_fraction)
        self.add_arg("shipmode", self.get_shipmode, self.additional_ship)
        self.add_arg("word1", self.get_word1)
        self.add_arg("word2", self.get_word2)
        self.add_arg("brand", self.get_brand, self.additional_brand)
        self.add_arg("container", self.get_container)
        self.add_arg("cc", self.get_cc, self.additional_cc)

    def get_delta(self):
        return 90
        return random.randint(60, 120)

    def get_size(self, ign = None):
        return random.randint(1, 50)

    def additional_size(self):
        rep = 0
        if self.num == 16:
            rep = 8
        return True, rep

    def get_type(self):
        if self.num == 2:
            return random.choice(types[2])
        if self.num == 16:
            return self.random_choice_prod(types[0], types[1])
        return self.random_choice_prod(*types)

    def get_region(self):
        if self.num == 8:
            nation = self.args["NATION"]
            region_key = nations[nation]
            return regions[region_key]
        return random.choice(regions)

    def get_segment(self):
        return random.choice(["AUTOMOBILE", "BUILDING", "FURNITURE", "MACHINERY", "HOUSEHOLD"])

    def random_date(self, start, end, freq='MS'):
        choices = pd.date_range(start, end, freq=freq)
        res = random.choice(choices)
        return res.date().isoformat()

    def get_date(self):
        if self.num == 3:
            return f"1995-03-{random.randint(1, 31)}"
        if self.num in [4, 15]:
            return self.random_date('1993-01-01', '1997-10-01')
        if self.num in [5, 6, 12, 20]:
            return f"{random.randint(1993, 1997)}-01-01"
        if self.num == 10:
            return self.random_date('1993-02-01', '1995-01-01')
        if self.num == 14:
            return self.random_date('1993-01-01', '1997-12-01')
        return None

    def get_discount(self):
        return random.uniform(0.02, 0.09)

    def get_quantity(self, idx = 0):
        if self.num == 18:
            return random.randint(312, 315)
        if self.num == 19:
            a = idx * 10
            if idx == 0:
                a = 1
            return random.randint(a, (idx + 1)*10)
        return random.randint(24, 25)

    def additional_quantity(self):
        rep = 0
        if self.num == 19:
            rep = 3
        return True, rep

    def get_nation(self, ign = None):
        return random.choice(list(nations.keys()))

    def additional_nation(self):
        rep = 0
        if self.num == 7:
            rep = 2
        return True, rep

    def get_color(self):
        return random.choice(["almond", "antique", "aquamarine", "azure", "beige", "bisque", "black", "blanched", "blue", "blush", "brown", "burlywood", "burnished", "chartreuse", "chiffon", "chocolate", "coral", "cornflower", "cornsilk", "cream", "cyan", "dark", "deep", "dim", "dodger", "drab", "firebrick", "floral", "forest", "frosted", "gainsboro", "ghost", "goldenrod", "green", "grey", "honeydew", "hot", "indian", "ivory", "khaki", "lace", "lavender", "lawn", "lemon", "light", "lime", "linen", "magenta", "maroon", "medium", "metallic", "midnight", "mint", "misty", "moccasin", "navajo", "navy", "olive", "orange", "orchid", "pale", "papaya", "peach", "peru", "pink", "plum", "powder", "puff", "purple", "red", "rose", "rosy", "royal", "saddle", "salmon", "sandy", "seashell", "sienna", "sky", "slate", "smoke", "snow", "spring", "steel", "tan", "thistle", "tomato", "turquoise", "violet", "wheat", "white", "yellow"])

    def get_fraction(self):
        return 0.0001 / float(self.sf)

    def get_shipmode(self, ign = None):
        return random.choice(["REG AIR", "AIR", "RAIL", "SHIP", "TRUCK", "MAIL", "FOB"])

    def additional_ship(self):
        rep = 0
        if self.num == 12:
            rep = 2
        return True, rep

    def get_word1(self):
        return random.choice(["special", "pending", "unusual", "express"])

    def get_word2(self):
        return random.choice(["packages", "requests", "accounts", "deposits"])

    def get_brand(self, ign = None):
        return f"Brand#{random.randint(1, 5)}{random.randint(1, 5)}"

    def additional_brand(self):
        rep = 0
        if self.num == 19:
            rep = 3
        return True, rep

    def get_container(self):
        return self.random_choice_prod(*containers)

    def get_cc(self, ign = None):
        countries = list(nations.keys())
        countries.sort()
        idx = random.randint(0, len(countries)-1)
        return idx + 10

    def additional_cc(self):
        rep = 0
        if self.num == 22:
            rep = 7
        return True, rep
        

def load_queries(path = "queries") -> [query]:
    ret = []
    for f in os.listdir(path):
        q = query(os.path.join(path, f))
        logger.debug("Preprocessed query: %s", q.get_sql())
        logger.debug("Posprocessed query: %s", q.get_sql(True))
        ret.append(q)
    ret.sort(key=lambda x: x.num)
    return ret


if __name__ == "__main__":
    load_queries("queries")