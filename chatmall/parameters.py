import time

localtime = time.asctime(time.localtime(time.time())).split()
mounth = localtime[1]
date = localtime[2]
year = localtime[4]
clock = localtime[3]
print(f"{mounth}-{date}-{year} {clock}")