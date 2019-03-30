import matplotlib.pyplot as plt
import numpy as np

x = [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]
x.extend([0] * 187)

#for part E
# x = [-1, -1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1]
# x.extend([0] * 185)

xd = np.zeros((200))
for i in np.arange(199, -1, -1):
    if i - 20 >= 0:
        xd[i] = x[i - 20]
    else:
        xd[i] = 0
plt.subplot(221)
plt.plot(range(200), x)

#replace 0.01 with 0.1, 1 (for part D)
v = np.random.normal(0, np.sqrt(0.01), 200)
y = 0.9 * xd + v
plt.subplot(222)
plt.plot(range(200), y)
result = np.zeros((60))
for i in range(60):
    for j in range(i, 60):
        result[j - i] += x[i] * y[j]
plt.subplot(223)
plt.plot(range(60), result)
plt.show()
