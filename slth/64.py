import matplotlib.pyplot as plt
import numpy as np

h = np.zeros((100))
h[0] = 1
y = np.zeros((100))
y3 = np.zeros((100))
y3[0] = 1 / 4
y3[1] = 1 / 2
y3[2] = 1 / 4
v = y3 + h
print(v)
y[0] = v[0]
y[1] = 0.9 * y[0] + v[1] + v[0]
for i in range(2, 100):
    y[i] = 0.9 * y[i - 1] - 0.81 * y[i - 2] + v[i] + v[i - 1]
plt.plot(range(100), y)
plt.show()
