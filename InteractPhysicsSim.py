# Pendulum.py
# -> Attempt to create a pendulum simulation in pyglet.
# Author: Justin Bunting
# Created: 2026/03/30
# Last Modified: 2026/04/13 08:47


from math import sin, cos, radians
import platform

import pyglet
from pyglet.window import key, mouse

from Shapes import *
from System import *
import EOMs


# 	initialize window

winSize = 1500 # on Mac, screen coords and render coords differ: want half-size window
winScale = 2 if platform.system() == 'Darwin' else 1
window = pyglet.window.Window(
	width=winSize//winScale,
	height=winSize//winScale,
	visible=True,
	resizable=False, # if resizing is desired, set to True and uncomment event below
	caption='Physics Simulations'
)


# 	Set EOM values (shared across functions)

origin = (winSize//2, winSize//2)
currentScene = None

# uncomment to modify!
# EOMs.mass = [20, 20] # kg
# EOMs.length = [3, 3] # m
# EOMs.gravity = 9.81 # m/s^2
# EOMs.gamma = (1.3, 1.3) # kg s^-1
# EOMs.k = (400, 400) # kg s^-2


# 	init system and define each scene

# set up the system (default has a pendulum running in the background, but no image)
pSys = PhysicsSystem(function=EOMs.pendulum, x0=[radians(20), 0])

# scene loader based on key press
def loadScene(symbol):
	global currentScene
	currentScene = symbol
	
	# render values
	pxLength = [l * metersToPixels for l in EOMs.length]
	startingAngle = [-40, 45]
	
	# load each physics system
	if symbol is key._1: # in (key._1, key._2):
		# set initial conditions and equation
		x0 = [radians(startingAngle[0]), 0]
		# if symbol is key._1:
			# pSys.reset(EOMs.pendulum, x0)
		# else:
		pSys.reset(EOMs.dampedPendulum, x0)
		
		# generate objects (and set anchors as defined by problem)
		basePoint = Point(	origin[0], origin[1], radius=15)
		bar = 		Bar(  	origin[0], origin[1], pxLength[0], rotationAnch=180)
		endPoint1 =  Point(	origin[0], origin[1], radius=EOMs.mass[0], yAnch=-pxLength[0], rotationAnch=180, color=(255, 255, 255, 255))
		endPoint2 = Point(	origin[0], origin[1], radius=EOMs.mass[0]-5, yAnch=-pxLength[0], rotationAnch=180, color=(200, 30, 30, 255))
		trail = 	FadeLine(0, 0, colors=((179, 224, 83, 255), (60, 60, 60, 0)), captureRate=1, strokeWidth=4, maxPoints=50)
		
		# attach objects
		pSys.addObject(trail, 1)
		pSys.addObject(bar)
		pSys.addObject(basePoint) # add after bar to appear above
		pSys.addObject(endPoint1)
		pSys.addObject(endPoint2)
		
		# add update actions
		pSys.addAction(bar.setAngle)
		pSys.addAction(endPoint1.setAngle)
		pSys.addAction(endPoint2.setAngle)
		pSys.addAction(trail.addPoint, 0, [('a2posVert', EOMs.length[0]), 'm2px', ('offsetPos', origin)])
		
		# set simulation values
		pSys.setArgument((0, 0), 'impulseXY', tuple[float, float], False) # impulse is NOT persistent
		# if symbol is key._2:
		pSys.setArgument(EOMs.gamma[0], 'gamma', float)
		
	elif symbol is key._2:
		# set initial conditions and equation -> use length, not pxLength
		x0 = [EOMs.length[0], 0, radians(startingAngle[0]), 0]
		pSys.reset(EOMs.springPendulum, x0)
		
		# generate objects (and set anchors)
		basePoint = Point(	origin[0], origin[1], radius=15)
		spring = 	Spring(	origin[0], origin[1], pxLength[0], rotationAnch=180)
		endPoint1 = Point(	origin[0], origin[1], radius=EOMs.mass[0], yAnch=-pxLength[0], rotationAnch=0, color=(255, 255, 255, 255))
		endPoint2 = Point(	origin[0], origin[1], radius=EOMs.mass[0]-5, yAnch=-pxLength[0], rotationAnch=0, color=(200, 30, 30, 255))
		trail = 	FadeLine(0, 0, colors=((240, 155, 64, 255), (60, 60, 60, 0)), captureRate=1, strokeWidth=4, maxPoints=300)
		
		# attach objects
		pSys.addObject(trail, 1)
		pSys.addObject(spring)
		pSys.addObject(basePoint) # add after spring to appear above
		pSys.addObject(endPoint1)
		pSys.addObject(endPoint2)
		
		# add update actions
		pSys.addAction(trail.addPoint, [0, 2], ['rth2xy', 'm2px', ('offsetPos', origin)])
		pSys.addAction(spring.setLength, 0, ('m2px',))
		pSys.addAction(spring.setAngle, 2)
		pSys.addAction(endPoint1.setAnchorY, 0, ('m2px',))
		pSys.addAction(endPoint1.setAngle, 2)
		pSys.addAction(endPoint2.setAnchorY, 0, ('m2px',))
		pSys.addAction(endPoint2.setAngle, 2)
		
		# set simulation values
		pSys.setArgument((0, 0), 'impulseXY', tuple[float, float], False) # impulse is NOT persistent
		pSys.setArgument(EOMs.gamma, 'gamma', tuple[float, float])
		pSys.setArgument(EOMs.k, 'k', float)
	
	elif symbol is key._3:
		# set initial conditions and equation
		x0 = [radians(startingAngle[0]), 0, radians(startingAngle[1]), 0] # theta, thetaDot, alpha, alphaDot
		pSys.reset(EOMs.doublePendulum, x0)
		
		# generate objects (and set anchors)
		midLoc = (origin[0] + pxLength[0] * sin(radians(startingAngle[0])), origin[1] - pxLength[0] * cos(radians(startingAngle[0])))
		basePoint = Point(	origin[0], origin[1], radius=15)
		bar1 = 		Bar(  	origin[0], origin[1], length=pxLength[0], rotationAnch=180)
		midPoint =	Point(	origin[0], origin[1], radius=EOMs.mass[0], yAnch=pxLength[0], rotationAnch=0, color=(255, 255, 255, 255))
		bar2 =		Bar(	midLoc[0], midLoc[1], length=pxLength[1], rotationAnch=180)
		endPoint1 = Point(	midLoc[0], midLoc[1], radius=EOMs.mass[1], yAnch=pxLength[1], rotationAnch=0, color=(255, 255, 255, 255))
		endPoint2 = Point(	midLoc[0], midLoc[1], radius=EOMs.mass[1]-5, yAnch=pxLength[1], rotationAnch=0, color=(200, 30, 30, 255))
		trail = 	FadeLine(0, 0, colors=((229, 64, 115, 255), (60, 60, 60, 0)), captureRate=1, strokeWidth=4, maxPoints=300)
		
		# attach objects (bars first to render points above)
		pSys.addObject(trail, 1)
		pSys.addObject(bar1)
		pSys.addObject(bar2)
		pSys.addObject(basePoint)
		pSys.addObject(midPoint)
		pSys.addObject(endPoint1)
		pSys.addObject(endPoint2)
		
		# add update actions
		pSys.addAction(bar1.setAngle, 0)
		pSys.addAction(midPoint.setAngle, 0)
		pSys.addAction(bar2.setPosition, 0, [('a2posVert', EOMs.length[0]), 'm2px', ('offsetPos', origin)])
		pSys.addAction(endPoint1.setPosition, 0, [('a2posVert', EOMs.length[0]), 'm2px', ('offsetPos', origin)])
		pSys.addAction(endPoint2.setPosition, 0, [('a2posVert', EOMs.length[0]), 'm2px', ('offsetPos', origin)])
		pSys.addAction(bar2.setAngle, 2)
		pSys.addAction(endPoint1.setAngle, 2)
		pSys.addAction(endPoint2.setAngle, 2)
		pSys.addAction(trail.addPoint, [0, 2], [('a2posVert', EOMs.length[0], EOMs.length[1]), 'sum2', 'm2px', ('offsetPos', origin)])
		
		# set simulation values
		pSys.setArgument((0, 0), 'impulseXY', tuple[float, float], False) # impulse is NOT persistent
		pSys.setArgument(EOMs.gamma, 'gamma', tuple[float, float])
		

#	interaction setup (click impulse, hidden list)

clickImpulse = False
clickStart = 0, 0
arrow = Arrow(0, 0, 5)
arrow.setVisible(False)

hidden = {1}


#	finish pyglet setup (update, event handlers, run)

def update(dt):
	pSys.update(dt) # can get time and x (state) out of this function if wanted

@window.event
def on_key_press(symbol, modifiers):
	global hidden
	
	# switch system
	if symbol in (key._1, key._2, key._3): #, key._4, key._5, key._6, key._7, key._8):
		loadScene(symbol)
	
	# control visibility for better visuals
	if symbol is key.BRACKETLEFT:
		hidden ^= {0}
	elif symbol is key.BRACKETRIGHT:
		hidden ^= {1}
	pSys.setVisible(hiddenGroups=hidden)
	
	# quick-close because clicking is slow at times..?
	if symbol is key.ESCAPE:
		pyglet.app.exit()

@window.event
def on_mouse_press(x, y, buttons, modifiers):
	global clickStart, clickImpulse, arrow
	if buttons & mouse.LEFT:
		clickStart = x, y
		clickImpulse = True
	
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
	global arrow
	if buttons & mouse.LEFT and clickImpulse:
		arrow.setPosLen(x, y, clickStart[0] - x, clickStart[1] - y)
		arrow.setVisible(True)

@window.event
def on_mouse_release(x, y, buttons, modifiers):
	global clickImpulse, force, arrow
	if buttons & mouse.LEFT and clickImpulse:
		magBase = 50 # N/px
		dx = (clickStart[0] - x)
		dy = (clickStart[1] - y)
		force = (dx * magBase, dy * magBase)
		
		pSys.setArgument(force, 'impulseXY')
		clickImpulse = False
		arrow.setVisible(False)

# uncomment if window resizing is needed.. doesn't play well with Aerospace app on Mac
# also, don't forget to set resizeable=True up top in window

# def _reloadAfterResize(dt):
# 	global winSize, winScale, origin
# 	# snap window to square using the smaller dimension
# 	size = min(window.width, window.height)
# 	window.set_size(size, size)
# 	winSize = size * winScale
# 	origin = (winSize // 2, winSize // 2)
# 	if currentScene is not None:
# 		loadScene(currentScene)
	
# @window.event
# def on_resize(width, height):
# 	# debounce: each resize event reschedules the reload, so it only fires once the user
# 	# stops dragging
# 	pyglet.clock.unschedule(_reloadAfterResize)
# 	pyglet.clock.schedule_once(_reloadAfterResize, 0.25)
# 	return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
	window.clear()
	
	# draw arrow first because force in background looks best
	arrow.draw()
	pSys.draw()


# 	run app

if __name__ == "__main__":
	# schedule our update function
	pyglet.clock.schedule_interval(func=update, interval=1/60)
	pyglet.app.run()