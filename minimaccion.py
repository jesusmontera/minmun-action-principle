import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from BezierCurve import *
import random
# muestra en animacion como la accion del tiro parabólico es siempre menor
# que cualqier otro camino escogido al azar (curva bezier)

class tiroParabolico:
    def __init__(self, n=100,angle=37,v0=10,tf=2,x0=0,y0=0):
        
        theta=np.radians(angle)
        
        self.g=9.8
        self.v0=v0
        t=np.linspace(0,tf,n)
        self.x=x0+v0*np.cos(theta)*t
        self.y=y0+(v0*np.sin(theta)*t) - 0.5 * self.g * t**2
        self.t=t

    
    def calc_UEc(self,mass):
        # calculate V and Ec by dt step and speed by hand
        n = len(self.x)
        Ec= np.zeros(n)
        U= np.zeros(n)
        Ec[0]=0.5 * mass * self.v0**2
        U[0]=mass * self.y[0] * self.g
        
        dt = self.t[1]-self.t[0]
                
        for i in range(1,n,1):
            dx=self.x[i]-self.x[i-1]
            dy = self.y[i]-self.y[i-1]            
            dg = 0.5 * self.g * dt**2
            dy +=dg # add to dy the distance that gravity pulled down in that dt interval
            speed=np.sqrt(dx**2+dy**2)/dt
            Ec[i]=0.5 * mass * speed**2
            U[i] = mass * self.y[i] * self.g
        return Ec,U
    
    def setPath(self,curve):
        # just for testing bezier curve path minimum action principle
        # first call this function with a bezier curve that ends and starts in the same points
        # that the original parabolic path and then call calc_UEc to get U and Ec from bezier curve
        
        for i in range(1,n,1):
            self.x[i]=curve[i-1][0]
            self.y[i]=curve[i-1][1]
            
            
    def Energies(self,mass):
        # calculate Ec by U by energy conservation(E = U + Ec)
        g=9.8
        E = 0.5 * mass *self.v0**2  # inital energy that is conserved                  
        U = mass * self.y * g
        Ec = E - U
        return Ec,U



    

mass=1.0
tf=2.0
n=201
tp= tiroParabolico(n=n,angle=37,v0=16.3,tf=tf,x0=0,y0=0)
fig, ax=plt.subplots()
plt.plot(tp.x,tp.y, label="tiro parabol")

Ec,U= tp.Energies(mass) # simplest method to calc U and Ec
Ec2,U2=tp.calc_UEc(mass) # just to test if calc_UEc give same values than above method
dt = tf/n
S1=sum((Ec-U)*dt)
print("S accion por E=",S1)
print("S accion by dt step=",sum((Ec2-U2)*dt))



# create a random path with a bezier curve that uses 4 points (start, control 1, control 2 and end)
# you can change control 1 and control2 to make a diferent path for testing minimum action principle
# action must always be bigger than the original parabolic
bzpx=[tp.x[0],tp.x[n//4],tp.x[(n//4)*3] , tp.x[n-1]]
bzpy=[tp.y[0],tp.y[n//4],tp.y[(n//4)*3] , tp.y[n-1]]
def changePath(rx,ry):
    # rx and  ry random variables to change curve path
    bezier_curve = BezierCurve(n-2)
    bezier_curve.add_point(bzpx[0], bzpy[0]) # start
    bezier_curve.add_point(bzpx[1]*rx, bzpy[1]*ry) # control 1    
    bezier_curve.add_point(bzpx[2]*rx, bzpy[2]*ry) # control 2    
    bezier_curve.add_point(bzpx[3], bzpy[3]) # end
    curve = bezier_curve.curve()    
    tp.setPath(curve)
changePath(1,1)
ln, = plt.plot(tp.x,tp.y, label="bezier \npath")

Ec3,U3=tp.calc_UEc(mass)
S3=sum((Ec3-U3)*dt)
print("S accion by bezier curve=",S3)
ax.set_title("ACCCION(S)    S parabol "+ str(int(S1)) + "    S bezier " + str(int(S3)))

#plt.plot(curve[:, 0], curve[:, 1],label="bezier path")
plt.legend(loc='upper right')



def actualizar(i):
    ry=random.uniform(0.3, 2.)
    rx=random.uniform(0.7, 1.3)
    changePath(rx,ry)
    ln.set_data(tp.x,tp.y)
    Ec3,U3=tp.calc_UEc(mass)
    S3= sum((Ec3-U3)*dt)
    ax.set_title("ACCCION(S)    S parabol "+ str(int(S1)) + "    S bezier " + str(int(S3)))
    
    return ln,
ani = animation.FuncAnimation(fig,actualizar,interval=1000)
plt.show()

