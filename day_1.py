f = open("/home/thomas/Skrivbord/Programmering/advent_of_code/day_1_data.txt")

ans = 0

for line in f.readlines():
    ans += int(int(line)/3) - 2

print(ans)

f.close()


f = open("/home/thomas/Skrivbord/Programmering/advent_of_code/day_1_data.txt")

ans = 0
x = 0



for line in f.readlines():
    x = int(line)
    while x >= 0:
        x = int(x/3) - 2
        if x >= 0:
            ans += x

f.close()

print(ans)