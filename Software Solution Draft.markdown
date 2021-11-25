# Software Solution Draft - Mechanical solution counterpart

## General Process

1. Be started via a button press on the robot
2. Assume it's in a starting zone in the pre-defined arena
3. Store apriltag for it's scoring zones
3. Travel out of corner and face the middle of the arena
4. Start object recognition to move and acquire balls - keeping track of it's rotation
5. Once full, rotate to where it's scoring zone should be, find it's scording zones and deposit the balls into their appropriate area
6. Repeat from 4

- Can be stopped via the same button on the robot
- Should be able to take hits, shunts, rams without taking damage

## Specific Aspects
<details>
<summary>**Vehicle Control**</summary>

The robot needs to control itself within the arena to perform it's tasks.

A motor

</details>

<details>
<summary>**Position**</summary>

A crucial aspect of the task is to travel back to your starting position to deposit your acquired balls

<details>
<summary>**Recycled PS/2 Mouse**</summary>

Such 

**Pros**

- Promotes e-waste awareness

**Cons**

- In

</details>

<details>
<summary>**Inertial Measurement Unit (IMU) / Accelerometer, Gyroscope, Magnetometer**</summary>

Such devices measure a variety of forces acting on it, and can theoretically be used to track position. 

**Pros**

- Computationally simple
- Cheap

**Cons**

- In the real world, the hardware will have error, along with the implementing software and accuracy cannot be confirmed.
	- An IMU (or it's components) will have particular bias ("traits/characteristics") which theoretically could be identified and accounted for, but increases software complexity for going with a simpler hardware approach.
	- The application requires integration of the samples over time which as with all digital processing is always a compromise, and will induce error in software.

</details>

---

</details>

<details>
<summary>**Computer Vision**</summary>

Blah blahhhh

<details>
<summary>**Feature Tracking**</summary>

Spatial localisation and mapping (SLAM) operates on tracking features movement and localising the camera position in each frame to map it's path.

**Pros**

- Can use April Tags (fiduals) to perform SLAM to simplify feature recognition
- Would be pretty awesome
- Would put Jetson Nano to great use

**Cons**

- Relatively high frame rate would be preferable (5fps+)
- Computationally and technically complex

</details>

<details>
<summary>**Distance Triangulation**</summary>

Using ultrasonic distance sensors for example; positioning can be theoretically achieved by localising yourself

**Pros**

- 


**Cons**

- System could be occluded by other robots or objects in the arena leading to false distances
- More advanced implementations of this, such as the use of LiDar would better, but would be exceedingly expensive.

</details>

<details>
<summary>**Ball Detection**</summary>

In any design, some ball detection is can be implemented to optimise the acqusition of balls (instead of sweeping across the arena in a bruteforce manner).
In particular cases, further detection can be used to differentiate between tennis and ping pong balls. Perhaps for prioistration, or for sorting. (However sorting is likely to be majorly mechanically achieved, through the aid of software)

</details>

---

</details>

<details>
<summary>**I/O**</summary>

A variety of I/O will be incorporated, for example, the robot may have:

- Electronic speed controllers (ESCs)
- Inertial Measurement Unit (IMU)
- Servo actuators (for scooping, herding, sorting)
- Distance sensors (likely ultrasonic)
- Weight sensors (unlikely)

</details>

<details>
<summary>**Tricks**</summary>

- Have images of balls on our robot to fake out other camera recognition robots
- Steal other robots balls
- Acquire all balls in the arena irrelevant to type, and sort on-board the robot

</details>