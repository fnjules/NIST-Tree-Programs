from vpython import*
import random

#initial parameters
split=3
rounds=4
maxradius=1
radius=0.3
maxAttempts=1000

pairlst=[]#empty list to store endpoints of all branches


def setupEnvironment():
    #greate graph environment
    circGraph= graph(width=1000, height=1000,
        xmin=-1.1, xmax=1.1, ymin=-1.1, ymax=1.1,
        title="Tree Program", xtitle=f"split = {split}\t maxradius = {maxradius}\t length = {radius}\t rounds = {rounds}")
    #circle/origin setup
    f1 = gcurve(color=color.cyan)
    for theta in arange(0, 2*pi, 0.01):
        f1.plot(maxradius*cos(theta),maxradius*sin(theta))
    finit = gdots(color=color.red)
    finit.plot([0,0])


#variable for randomized angle
def randomAng_func():
    return 2*pi*(random.random())


def line(p1, p2): #some special math here to determine if intersection occurs again (Cramer's rule)
                A = (p1[1] - p2[1])
                B = (p2[0] - p1[0])
                C = (p1[0]*p2[1] - p2[0]*p1[1])
                return A, B, -C


def intersection(L1, L2):
                D  = L1[0] * L2[1] - L1[1] * L2[0]
                Dx = L1[2] * L2[1] - L1[1] * L2[2]
                Dy = L1[0] * L2[2] - L1[2] * L2[0]
                if D != 0:
                  Xi = Dx / D
                  Yi = Dy / D
                  return Xi, Yi #return distance of intersection segment
                else:
                  return False


def checkIntersect(origin, target): #checks for "intersections"
    Xo, Yo = origin
    L1 = line(origin, target)
    for segment in pairlst:
        X1, X2 = segment[0][0], segment[1][0]
        L2 = line(segment[0],segment[1])
        R = intersection(L1,L2)
        if R:
            Xi, Yi = R #"intersection" point found
            if ((Xi > min(Xo,target[0]) and Xi < max(Xo,target[0])) and (Xi > min(X1,X2) and Xi < max(X1,X2))): #Xi lies in x-intervals, real intersection exists
                d = sqrt((Xi-Xo)**2+(Yi-Yo)**2) #calculates distance to intersection point
                if d > 10**(-10):
                    print (f'intersection point is {[Xi, Yi]}, {d}')
                    return [d, Xi, Yi] #returns distance and intersection coordinate pair
                else:
                    continue
            else: 
                continue
    return False


def branch(origin):
    Xo, Yo = origin
    tmplst=[] #for output
    scale1 = 1 
    thickness = 1 - roundNumber/(rounds+1)
    for i in range(split):
        intersection_exists = False
        theta = randomAng_func() #choose angle randomly
        target=[scale1*radius*cos(theta)+Xo,scale1*radius*sin(theta)+Yo]#create target point
        q = sqrt( (scale1*radius*cos(theta))**2 + (scale1*radius*sin(theta))**2 ) #checks original radius distance
        print(f'q is {q}')
        if target[0]**2+target[1]**2 > maxradius**2: #exit immediately if point is outside of graph
            continue
        if len(pairlst)<split: #makes ures to draw split# of branches
            gcurve(markers=True, width=3*thickness, marker_color = color.red, color = color.black).plot([origin,target])
            print(f'round {roundNumber}, node {nodeNumber}, segment {i+1} drawn')
            tmplst.append(target)
            pairlst.append([origin,target])
            continue
        while checkIntersect(origin, target): #if real intersection exists, create target point halfway
            int_result = checkIntersect(origin, target)
            d = 0.5*int_result[0]
            target = [scale1*d*cos(theta)+Xo,scale1*d*sin(theta)+Yo]
            intersection_exists = True
        gcurve(markers=True, width=6*thickness, marker_color=color.red, color = color.black).plot([origin,target]) #plot halfway points
        tmplst.append(target)
        pairlst.append([origin,target])

        if intersection_exists:
            target2=[int_result[1],int_result[2]] #create intersection as target point
            while checkIntersect (origin, target2): #even if real intersection exists, create target point at intersection
                dd=checkIntersect(origin, target2)
                target2=[dd[1],dd[2]]
            gcurve(markers=True, width=3*thickness, marker_color=color.green, color = color.black).plot([origin,target2]) #plot intersection points
            print(f'round {roundNumber}, node {nodeNumber}, segment {i+1} extra branch drawn')
            pairlst.append([origin,target2])
        continue
    return tmplst



def drawTree(currentRound, originLst):
    if currentRound==0:
        print('Drawing complete.')
        return None
    else:
        global roundNumber
        global nodeNumber
        roundNumber = rounds - currentRound+1
        nodeNumber = 0
        tmp=[]
        for point in originLst:
            tmp += branch(point)
            nodeNumber += 1
        drawTree(currentRound-1, tmp)


if __name__ == "__main__":
    setupEnvironment()
    drawTree(rounds, [[0,0]])
