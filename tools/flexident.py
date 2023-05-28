import sys
import os
from struct import *

SECLEN = 256


f=open(sys.argv[1], 'rb')
print("File: %s" % sys.argv[1])
# Seek to 3rd sector in disk image
f.seek(2*SECLEN, 0)
data = f.read(48)
"""
H    14s  11s    H       B        B        B       B       H       B    B    B     B      B     8s
"""
link, zeros, volnam, volnum, first_t, first_s, last_t, last_s, numsec, mon, day, year, max_t, max_s, _ = \
    unpack(">H14s11sHBBBBHBBBBB8s", data) 
# print(link, volnam, volnum, first_t, first_s, last_t, last_s, numsec, mon, day, year, max_t, max_s)
flex=False
if link != 0:
    print("Not a FLEX disk")
#elif zeros != b'\x00'*14:
#    print("Not a FLEX disk")
else:
    flex=True

if not flex:
    exit()

print("Volume Name: %s"% volnam)
print("Volume Number: %d"% volnum)
print("Tracks: %d"% (max_t+1))
print("Sectors: %d"% max_s)
# Seek to end of sector
f.seek(SECLEN-48, 1)
# Seek to 11th sector in disk image
f.seek(SECLEN*7, 1)
t=0
t0s=10
while t==0:
    data = f.read(4)
    t,s,nxt = unpack(">BBH", data)
    # print(t0s, t,s,nxt)
    f.seek(SECLEN-4, 1)
    if t==0 and s==0 and nxt==1:
        break
    if t != 1:
        t0s += 1

if max_s in [10,20]:
    print("Single-Density")
    density="SD"
elif max_s in [17,18,36]:
    print("Double-Density")
    density="DD"
else:
    print("Density: Unknown")
    density="UD"

if max_s in [10,17,18]:
    print("Single-Sided")
    sides="SS"
elif max_s in [20,36]:
    print("Double-Sided")
    sides="DS"


st = os.stat(sys.argv[1])
csize = (t0s*SECLEN) + (max_t*max_s*SECLEN)
print("Image Size: %d" % st.st_size)
print("Calc Size: %d" % csize)
if(st.st_size != csize):
    print("ERROR: Size does not match")
    exit()

print("Track0: ", end='')
padding = True
if t0s in [10, 20]:
    print("Not ", end='')
    padding = False
#elif density == 'DD' and t0s in [18, 36]:
#    print("Not ", end='')
#    padding = False
else:
    padding = True

if sides=="DS":
    t0s /= 2

print("Padded, %d Sectors" % t0s)

cmd = ["./dmk.py", "--flex"]
if padding:
    cmd += ["--padding", "%d" % (t0s)]
cmd += ["--template", "BLANK_FLEX_%s%s%dT.DMK" % (sides, density, (max_t+1))]
cmd += ["--import", sys.argv[1]]
cmd += ["--output", "test.dmk"]

print(" ".join(cmd))
