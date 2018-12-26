# -*- coding: utf-8 -*-


import json
import re

str = "fdsaf{fdslfjdslfs}as{aaa"



list = re.findall(r'\{(.*)\}', str)

print(list[0])