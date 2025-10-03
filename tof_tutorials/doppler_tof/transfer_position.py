import numpy as np

# t=0时刻的4x4矩阵
mat0 = np.array([
    [-1, 0, 0, 0],
    [0, 1, 0, 1],
    [0, 0, -1, 6.8],
    [0, 0, 0, 1]
])

# t=0.0015时刻的4x4矩阵
mat1 = np.array([
    [-1, 0, 0, 0],
    [0, 1, 0, 1],
    [0, 0, -1, 6.9],
    [0, 0, 0, 1]
])

# 提取平移分量（最后一列的前三个数）
pos0 = mat0[:3, 3]
pos1 = mat1[:3, 3]

dt = 0.0015  # 秒
velocity = (pos1 - pos0) / dt

print("sensor_velocity参数为：", velocity.tolist())