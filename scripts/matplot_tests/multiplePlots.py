import matplotlib.pyplot as plt
import random
series = []
SERIESCANT = 10
SERIECANT = 100
plt.figure(1)
for i in range(SERIESCANT):
    aux_array = []
    for j in range(SERIECANT):
        aux_number = random.random()
        aux_array.append(aux_number)
    series.append(aux_array)
for i in range(SERIESCANT):
    plt.plot(series[i], label = 'Serie: ' + str(i))
plt.legend(loc = 'upper left')
plt.figure(2)
for i in range(SERIESCANT):
    aux_array = []
    for j in range(SERIECANT):
        aux_number = random.random()
        aux_array.append(aux_number)
    series.append(aux_array)
for i in range(SERIESCANT):
    plt.plot(series[i], label = 'Serie: ' + str(i))
plt.legend(loc = 'upper left')
plt.show()
