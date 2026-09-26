# -*- coding: utf-8 -*-
"""Python 第一天：只需 Python，不需要第三方包。"""
print(2 + 3)
x = 4
print(x + 2)
print(x)  # x 仍为 4
values = [2, 4, 6]
print(values[0])  # Python 下标从 0 开始
print(sum(values) / len(values))
def square(value):
    return value * value
print([square(v) for v in values])
# 练习：把 values 改成 [3,6,9]，先猜再运行。
