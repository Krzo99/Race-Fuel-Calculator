% Calculate Best race strategy!
% User Input
raceLength = 150;               % In Min
fuelCapacity = 120;             % In Liters  
pitDelay = 60;                % In Seconds 

avgLapTimeM1 = 1*60+45;         % In Seconds  
avgLapTimeM2 = 1*60+47;         % In Seconds 

fuelPerLapM1 = 2.9;             % In Liters  
fuelPerLapM2 = 2.75;             % In Liters 

numOfPointsToCalc = 300;        % In Ints

%End Of User Input

close all

maxLapsM1 = ceil(raceLength * 60 / avgLapTimeM1);
maxLapsM2 = ceil(raceLength * 60 / avgLapTimeM2);

lapsM1_array = linspace(0, maxLapsM1, numOfPointsToCalc);
lapsM2_array = linspace(0, maxLapsM2, numOfPointsToCalc);


timeDriven = @(Nm1, Nm2) (avgLapTimeM1 * Nm1 + avgLapTimeM2 * Nm2 + floor((Nm1 * fuelPerLapM1 + Nm2 * fuelPerLapM2) / fuelCapacity) * pitDelay);
avgLapTime = @(Nm1,Nm2) (timeDriven(Nm1, Nm2) / (Nm1 + Nm2));
numOfLaps = @(Nm1,Nm2) (raceLength * 60) / (avgLapTime(Nm1, Nm2));

[X,Y] = meshgrid(lapsM1_array, lapsM2_array);
Z = zeros(numOfPointsToCalc, numOfPointsToCalc);
for fm1 = 1:length(lapsM1_array)
    for fm2 = 1:length(lapsM2_array)
        bTimeValid = isTimeValid(timeDriven(lapsM1_array(fm1), lapsM2_array(fm2)), raceLength, avgLapTime(lapsM1_array(fm1), lapsM2_array(fm2)));
        if bTimeValid == 0
           X(fm2, fm1) = NaN;
           Y(fm2, fm1) = NaN;
        else
            Z(fm2, fm1) = numOfLaps(lapsM1_array(fm1), lapsM2_array(fm2));
        end
            
    end
end

% 3D graph
figure;
surf(X,Y,Z, 'LineWidth',3)

[maxLaps, indexMaxLaps] = max(Z(:));
[howManyOnM2, howManyOnM1] = ind2sub(size(Z), indexMaxLaps);
onM1 = lapsM1_array(howManyOnM1);
onM2 = lapsM2_array(howManyOnM2);

xlabel("Laps on M1")
ylabel("Laps on M2")
zlabel("Total Laps")

fprintf("You can drive: %f laps\n", max(max(Z)));
fprintf("On Map 1: %f\n", onM1);
fprintf("On Map 2: %f\n", onM2);
fprintf("You will race: %f min\n", timeDriven(onM1, onM2) / 60);
fprintf("You need to pit: %d times\n", floor((onM1 * fuelPerLapM1 + onM2 * fuelPerLapM2) / fuelCapacity));
FuelLeft = (ceil((onM1 * fuelPerLapM1 + onM2 * fuelPerLapM2) / fuelCapacity) - ((onM1 * fuelPerLapM1 + onM2 * fuelPerLapM2) / fuelCapacity))*fuelCapacity;
fprintf("Fuel Left: %f L, Can only fill %f L on last pit\n", FuelLeft, fuelCapacity - FuelLeft);


% Fuel Left vs Laps
FuelLeft = zeros(1, floor(maxLaps));
L = 0:floor(maxLaps);
m1left = floor(onM1);
m2left = floor(onM2);

FuelLeft(1) = fuelCapacity;
for i = 2:length(L)
    if m1left > 0
        if FuelLeft(i-1) - fuelPerLapM1 <= 0
            FuelWeneedToReduceNextLap = fuelPerLapM1 - FuelLeft(i-1);
            FuelLeft(i) = fuelCapacity - FuelWeneedToReduceNextLap;
        else
            FuelLeft(i) = FuelLeft(i-1) - fuelPerLapM1;
        end
        m1left = m1left - 1;
    elseif m2left > 0
        if FuelLeft(i-1) - fuelPerLapM2 <= 0
            FuelWeneedToReduceNextLap = fuelPerLapM1 - FuelLeft(i-1);
            FuelLeft(i) = fuelCapacity - FuelWeneedToReduceNextLap;
        else
            FuelLeft(i) = FuelLeft(i-1) - fuelPerLapM2;
        end
        
        m2left = m2left - 1;
    else
        FuelLeft(i) = FuelLeft(i-1);
    end
    
end


figure;
plot(L, FuelLeft, 'r');
ylim([0, fuelCapacity]);
xlabel("Lap")
ylabel("Fuel Left")


function bIsValid = isTimeValid(time, raceLength, lapTime)
    if time > raceLength*60 && time - raceLength*60 < lapTime
        bIsValid = 1;
    else
        bIsValid = 0;
    end

end