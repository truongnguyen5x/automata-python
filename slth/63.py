import matplotlib.pyplot as plt
import numpy as np

#only part A
h = np.zeros((50))
h[0] = 0.866
h[1] = 0.8 * h[0]
for i in range(2, 50):
    h[i] = 0.8 * h[i - 1] - 0.64 * h[i - 2]
plt.subplot(221)
plt.plot(range(50), h)
plt.show()
