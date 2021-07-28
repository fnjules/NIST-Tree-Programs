GlowScript 3.1 VPython

import random

#initial parameters
split=6
maxround=0
maxradius=1
radius=0.4
maxAttempts=1000

angles = [i for i in range(0,360,.1)] #create list of all possible angles
#I don't think 360 is necessarily the right choice, but it works! for now..

#greate graph environment
circGraph= graph(width=500, height=500,
    xmin=-1.1, xmax=1.1, ymin=-1.1, ymax=1.1,
    title="Tree Program", xtitle=f"split = {split}\t maxradius = {maxradius}\t length = {radius}")

#circle/origin setup
f1 = gcurve(color=color.cyan)
for theta in arange(0, 2*pi, 0.01):
    f1.plot(maxradius*cos(theta),maxradius*sin(theta))
finit = gdots(color=color.red)
finit.plot([0,0])


pairlst=[]#empty list to store endpoints of all branches


def checkIntersect(newBranch):
    if len(pairlst)<split:
        return True
    X1=newBranch[0][0]
    Y1=newBranch[0][1]
    X2=newBranch[1][0]
    Y2=newBranch[1][1]
    
    #exit immediately if it is outside of circle
    if X2**2 + Y2**2 > maxradius**2:
        return False

    #continue for intersections with other line segments
    I1 = [min(X1,X2), max(X1,X2)]
    for segment in pairlst:
        X3=segment[0][0]
        Y3=segment[0][1]
        X4=segment[1][0]
        Y4=segment[1][1]
        I2 = [min(X3,X4), max(X3,X4)]
        Ia = [max(min(X1,X2), min(X3,X4)), min(max(X1,X2), max(X3,X4))]
        if (max(X1,X2) < min(X3,X4)):
            continue  # There is no mutual abcisses
        A1 = (Y1-Y2)/(X1-X2)  # Pay attention to not dividing by zero
        A2 = (Y3-Y4)/(X3-X4)  # Pay attention to not dividing by zero
        b1 = Y1-A1*X1
        b2 = Y3-A2*X3
        if (A1 == A2):
            continue  # Parallel segments
        Xa = (b2 - b1) / (A1 - A2)   # Once again, pay attention to not dividing by zero
        if ( (Xa < max( min(X1,X2), min(X3,X4) )) or (Xa > min( max(X1,X2), max(X3,X4) )) ):
            continue  # intersection is out of bound
        else:
            return False
    return True
    


def branch(origin):
    tmpangles = angles #temp copy of all angles
    tmplst=[] #for output
    Xo = origin[0]
    Yo = origin[1]
    for i in range(split):
        for j in range(maxAttempts):
            theta = random.choice(tmpangles) #choose angle randomly
            tmpangles.remove(theta) #remove it from list
            target=[radius*cos(theta)+Xo,radius*sin(theta)+Yo] #create target point  
            if checkIntersect([origin,target]): #if it is okay, draw it and move on. otherwise try again
                gcurve().plot(data=[origin,target])
                finit.plot(target)
                tmplst.append(target)
                pairlst.append([origin,target])
                print(f'segment {i+1} drawn')
                break
    return tmplst #return list of new endpoints from this origin



run1=branch([0,0])#start from origin origin
#the below line is not behaving nicely in for-loops to make it more automated...
#will need to manually adjust the counts per split number
run2=branch(run1[0])+branch(run1[1])+branch(run1[2])+branch(run1[3])+branch(run1[4])+branch(run1[5])#do it again for all 5 new points
