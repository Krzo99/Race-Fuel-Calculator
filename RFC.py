import matplotlib.pyplot as plt
import numpy as np

# Calculate Best race strategy!
# User Input
raceLength = 180               # In Min
fuelCapacity = 106             # In Liters
pitDelay = 17 + 40             # In Seconds

avgLapTimeM1 = 1*60 + 31.8     # In Seconds
avgLapTimeM2 = 1*60 + 32.3     # In Seconds

fuelPerLapM1 = 2.78            # In Liters
fuelPerLapM2 = 2.52            # In Liters

numOfPointsToCalc = 300        # In Ints

# End Of User Input

def timeDriven(Nm1, Nm2):
    return avgLapTimeM1 * Nm1 + avgLapTimeM2 * Nm2 + np.floor((Nm1 * fuelPerLapM1 + Nm2 * fuelPerLapM2) / fuelCapacity) * pitDelay


def avgLapTime(Nm1, Nm2):
    return timeDriven(Nm1, Nm2) / (Nm1 + Nm2)


def numOfLaps(Nm1, Nm2):
    return (raceLength * 60) / (avgLapTime(Nm1, Nm2))


def isTimeValid(time, laptime):
    if time > raceLength * 60 and time - raceLength * 60 < laptime:
        return True
    return False


maxLapsM1 = int(np.ceil(raceLength * 60 / avgLapTimeM1))
maxLapsM2 = int(np.ceil(raceLength * 60 / avgLapTimeM2))

lapsM1_array = np.linspace(0, maxLapsM1, numOfPointsToCalc)
lapsM2_array = np.linspace(0, maxLapsM2, numOfPointsToCalc)

X, Y = np.meshgrid(lapsM1_array, lapsM2_array)
Z = np.zeros((numOfPointsToCalc, numOfPointsToCalc))

for fm1 in range(len(lapsM1_array)):
    for fm2 in range(len(lapsM2_array)):
        bTimeValid = isTimeValid(timeDriven(lapsM1_array[fm1], lapsM2_array[fm2]),
                                 avgLapTime(lapsM1_array[fm1], lapsM2_array[fm2]))
        if bTimeValid == 0:
            Z[fm2, fm1] = np.nan
        else:
            Z[fm2, fm1] = numOfLaps(lapsM1_array[fm1], lapsM2_array[fm2])


# 3D graph

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour(X, Y, Z, numOfPointsToCalc)
ax.set_xlabel('Laps on M1')
ax.set_ylabel('Laps on M2')
ax.set_zlabel('Total Laps')
ax.invert_xaxis()
plt.show(block=False)

MaxLaps = np.nanmax(Z)
onM2_index, onM1_index = np.unravel_index(np.nanargmax(Z), Z.shape)
onM1 = lapsM1_array[onM1_index]
onM2 = lapsM2_array[onM2_index]

print("You can drive: {:.2f} laps".format(MaxLaps))
print("On Map 1: {:.2f}".format(onM1))
print("On Map 2: {:.2f}".format(onM2))
print("You will race: {:.2f} min".format(timeDriven(onM1, onM2) / 60))
print("You need to pit: {:.0f} times".format(np.floor((onM1 * fuelPerLapM1 + onM2 * fuelPerLapM2) / fuelCapacity)))
FuelLeft = (np.ceil((onM1 * fuelPerLapM1 + onM2 * fuelPerLapM2) / fuelCapacity) - ((onM1 * fuelPerLapM1 + onM2 * fuelPerLapM2) / fuelCapacity))*fuelCapacity
print("Fuel Left: {:.2f} L, Can only fill {:.2f} L on last pit".format(FuelLeft, fuelCapacity - FuelLeft))


# Fuel Left vs Laps
FuelLeft = np.zeros((int(np.floor(MaxLaps)) + 1))
L = np.linspace(0, int(np.floor(MaxLaps)), int(np.floor(MaxLaps)) + 1)
m1left = np.floor(onM1)
m2left = np.floor(onM2)

FuelLeft[0] = fuelCapacity
for i in range(1, len(L)):
    if m1left > 0:
        if FuelLeft[i - 1] - fuelPerLapM1 <= 0:
            FuelWeNeedToReduceNextLap = fuelPerLapM1 - FuelLeft[i - 1]
            FuelLeft[i] = fuelCapacity - FuelWeNeedToReduceNextLap
        else:
            FuelLeft[i] = FuelLeft[i - 1] - fuelPerLapM1
        m1left = m1left - 1
    elif m2left > 0:
        if FuelLeft[i - 1] - fuelPerLapM2 <= 0:
            FuelWeNeedToReduceNextLap = fuelPerLapM1 - FuelLeft[i - 1]
            FuelLeft[i] = fuelCapacity - FuelWeNeedToReduceNextLap
        else:
            FuelLeft[i] = FuelLeft[i - 1] - fuelPerLapM2

        m2left = m2left - 1
    else:
        FuelLeft[i] = FuelLeft[i - 1]

fig2 = plt.figure()
plt.plot(L, FuelLeft, '-o', markersize=5)
plt.ylim([0, fuelCapacity])
plt.xlabel("Lap")
plt.ylabel("Fuel Left")


plt.show()


