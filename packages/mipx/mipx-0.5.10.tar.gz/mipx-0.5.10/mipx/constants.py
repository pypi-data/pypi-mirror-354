# -*- coding: utf-8 -*-
# @Time    : 2023/3/31 22:21
# @Author  : luyi
from enum import Enum
from typing import Literal, Optional


P1, P2, P3, P4, P5, P6, P7, P8, P9 = (
    1,
    10,
    100,
    1000,
    10000,
    100000,
    1000000,
    10000000,
    100000000,
)


class Vtype(Enum):
    BINARY = "B"
    CONTINUOUS = "C"
    INTEGER = "I"


class ObjType(Enum):
    MINIMIZE = "MIN"
    MAXIMIZE = "MAX"


# optimization status
class OptimizationStatus(Enum):
    """求解器返回错误"""
    ERROR = -1

    """已计算出最优解"""
    OPTIMAL = 0

    """模型被证明无可行解"""
    INFEASIBLE = 1

    """目标函数中存在一个或多个变量未受约束条件限制，且最优目标值为无穷大"""
    UNBOUNDED = 2

    """在搜索过程中找到了整数可行解，但在确认该解是否为最优解前搜索被中断"""
    FEASIBLE = 3

    """松弛线性规划存在可行解，但带整数变量的问题无可行解"""
    INT_INFEASIBLE = 4

    """执行了截断搜索但未找到任何整数可行解"""
    NO_SOLUTION_FOUND = 5

    """问题已加载但未执行优化"""
    LOADED = 6

    """当前截断值下不存在可行解"""
    CUTOFF = 7

    """其他状态"""
    OTHER = 10000


class CmpType(Enum):
    LESS_EQUAL = 0
    EQUAL = 1
    GREATER_EQUAL = 2


class Params:
    def __init__(self):
        self.TimeLimit: Optional[int] = None  # 单位秒
        self.MIPGap: Optional[float] = None  # 表示多少的gap,0.10则表示10
        self.EnableOutput = False
        self.Precision: Optional[float] = None  # 精度控制
        self.CpoptimizerPath: Optional[str] = None  # Cplex约束求解器路径
