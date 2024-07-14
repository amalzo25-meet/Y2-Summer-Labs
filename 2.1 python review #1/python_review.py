import random

good_days_count = 0

aboveavg = []

temperature = []
for n in range(7):
    i = random.randint(26, 40)
    temperature.append(i)

days_of_the_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

print("The Weather Report:")

print("the even temperatures of the week:")

for v in range(7):
    if temperature[v] % 2 == 0:
        print(days_of_the_week[v] , "(", temperature[v], "c)")
        good_days_count += 1


highest_temp = max(temperature)
highindex = temperature.index(highest_temp)
highest_temp_day = days_of_the_week[highindex]

lowest_temp = min(temperature)
lowindex = temperature.index(lowest_temp)
lowest_temp_day = days_of_the_week[lowindex]


temp_sum = 0
avg = 0

for e in range(7):
	temp_sum += temperature[e]

avg = temp_sum/7

for t in range(7):
    if temperature[t] > avg:
        aboveavg.append(days_of_the_week[t])

print("Weekly temperature")

for x in range(7):
	print(days_of_the_week[x], ":", temperature[x])

print("*")

print("Shelly had", good_days_count, "good days")

print("*")

print("The hottest temperature was:", highest_temp, highest_temp_day)

print("The lowest temperature was:", lowest_temp, lowest_temp_day)

print("*")

print("The average temperature is:", avg)
print("The days above average are:", aboveavg)