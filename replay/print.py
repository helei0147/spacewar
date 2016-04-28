import os,sys
replay=open('replay1','r')
while True:
    character=replay.read(1)
    if len(character)==0:
        break
    mask=1
    character=ord(character)
    for i in range(8):
        if mask&character!=0:
            print 1,
        else:
            print 0,
        mask=mask<<1
    print
replay.close()
