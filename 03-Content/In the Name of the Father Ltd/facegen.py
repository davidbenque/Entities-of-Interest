# -*- coding: utf-8 -*-
# @Author: davidbenque
# @Date:   2018-06-16 19:42:42
# @Last Modified by:   davidbenque
# @Last Modified time: 2018-06-16 19:46:07

from random import choice as choice

faces = "🙍👵‍🙎‍👱👱👴👵👵👱👱🙎🙎👵👱👱👱👵👵👵👱"

s = ""
for n in range(4):
    for i in range(10):
        s += choice(faces)
    s += "<br>"

print(s)