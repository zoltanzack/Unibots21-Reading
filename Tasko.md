# Hardware
The hardware of the robot regards itself with all the electronic components of the robot. This would be hardware components such as the Jetson itself, and camera(s). Though also be regarding wiring the components, designing and creating any circuits needed to interface the Jetson with any components (servos, sensors, motors). This task will involve sourcing (researching and deciding on), wiring, and connecting components. The robot is expected to require the following:
- Motors
- Speed controllers
- Servos
- Camera (Compatible with Jetson Nano)
- Wiring/circuitry

# Mechanical
The mechanical aspect of the robot is every non-electronic physical aspect. Members of this task will be responsible for designing and creating the structure of the robot, including:
- Wheels and tyres
- Axel
- Mounting of hardware (motors, servos, battery, camera, Jetson)
- Flipper mount and control
- Mechanisms for acquiring and releasing the balls accurately and controlled
- Sturdy robot base
- Promoting up-cycling philosophies to support the reduction of e-waste.

# Software

## Group Decisions
How to not hit other robots, what to do when obstructed, what should happen if something obstructs it's path (i.e.: other robot)

## Personal Tasks
### Imole - Scoring
i.e.: When should the robot head to scoring zone, how should the robot head to scoring zone, how should balls to be dropped from the robot - physically (can look at robot model for familirsation with the current mechanism design), how to ensure balls are kept within their scoring zone (to remain eligible for bonus points)

Dropping off the balls, when to drop off the balls (conditions), how to drop off the balls, what to clear the conditions back to

### Joe - Ball acquisition and arena movement
Joe: Fetching the balls, what data is needed from the AI component, how many balls to obtain before returning to the scoring zone, what balls to prioritise, counting how many balls you have in the robot, differentiating between balls that are in someone's scoring zones or just in the arena

- Whether to go for both balls, or just one or the other at certain points in the round.
We cannot interefere with the robot while it's operating (expect to turn it off in an emergency)

### (Tentative) Ricc - Travelling
Ricc: How to return to the scoring zone, setting off when the round starts

Have a think about the below tasks that you have been assigned responsibility over (later make sure that you program this so it is customisable). Make sure you consider edge cases, scenarios, data needed to handle your task -->

# Other tasks
Redesign the robot in fusion 360 for a chance for us to win the best autodesk design prize

**Below is old notes about the task, may or may not be applicable now**
## Artificial Intelligence (Machine Learning and/or Traditional)
The intelligence of the robot isn’t restricted to descriptive or predicative methods. Though the tasks that are required to be performed are clear:
- Detecting and storing zone AprilTags
- Detecting tennis and ping pong ball locations
- Possibly: Detecting other robot locations and bounds
This task is more theoretically challenging rather than programmatically challenging. It’s roots are in Visual Intelligence and Image Analysis (both are modules in year 3). 

## Robot Control and Sensing
This task is programming the interface between all logic and the hardware. It does not handle when to perform a certain activity (operation framework), nor does it perform the logic of the robot. Rather, it’s the actor upon these two other aspects of the software implementation to realise the robot’s actions. Specifically, it’s responsible for:
- Controlling motor speed controllers
- Calculating robot position in the arena
- Planning the path back to base
- Aligning the robot with the two drop zones
- Manovering the robot around the arena towards balls
- Acquiring balls
- Dropping off balls into their zones
- Possibly: Avoiding other robots

## Execution strategy
Execution Strategy refers to the robot’s approach to a match. This task will tentatively involves:
- Design strategies the can robot take in a match
- Implementing these strategies programmatically for the robot to execute while in a match
- Accounting for certain stimuli.
- Some areas of research may include:
	- State machines
	- Expert (rule-based) systems