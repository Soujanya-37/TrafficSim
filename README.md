# 🚦 TrafficSim: A Command-Line Traffic Simulation

This is a simple traffic simulation built with Python and the Pygame library. It's a classic Computer Graphics and Visualization (CGV) project that models a single four-way intersection with functional traffic lights and autonomous cars.

## ✨ Features

### 🚀 Core Functionality

*Dynamic Traffic Lights: Two lights (one for vertical, one for horizontal) cycle automatically through green, yellow, and red states on a timer.

*Car Spawning: New cars are randomly spawned from all four directions at different intervals.

*Traffic Logic: Cars correctly stop for red and yellow lights at their designated stop lines.

*Collision Avoidance: Cars have a simple "sensor" and will stop to avoid colliding with another car directly in front of them in the same lane.

*Turning: Cars have a 50/50 chance of deciding to turn right at the intersection.

### 🎨 Visuals (Pygame UI)

*2D Graphics: Renders the roads, intersection, and stop lines in a clean, top-down 2D view.

*Animated Objects: Cars are represented by colored rectangles that move smoothly across the screen.

*Live Simulation: The simulation runs in real-time in its own window at 60 frames per second.

## 🛠️ Technologies Used

*Python 3

*Pygame (for graphics, animation, and windowing)

*Built-in Modules:

*time (for light cycles and spawn timing)

*random (for car colors, speeds, spawn times, and turn decisions)

## 🚀 How to Run (Getting Started)

*Prerequisites

You must have Python and the pip package manager installed.

*Installation

This project depends on the pygame library. You must install it from your Command Prompt (cmd) or Terminal:

#### ->pip install pygame


*Running the Simulation

Open your Command Prompt (cmd) or Terminal.

Navigate to the folder where you saved the file (e.g., your Downloads folder):

#### ->cd downloads


*Run the script using Python:

#### ->python TrafficSim.py


## 📖 How to Use

Once you run the command, a new Pygame window will open and the simulation will start automatically.

Cars will begin to spawn and move according to the traffic light rules.

To quit the simulation, simply close the Pygame window (click the "X").

## 🎯 Core Concepts Implemented

*Object-Oriented Programming (OOP): The simulation is built around a Car class and a TrafficLight class. Each object manages its own state (e.g., car.rect, light.state).

*Game Loop: Uses a standard while running loop that handles three distinct phases every frame:

*Event Handling: (Checking if the user clicked the "close" button).

*State Update: (Updating light timers, moving cars, checking for collisions).

*Drawing: (Clearing the screen and redrawing all roads, lights, and cars in their new positions).

*State Management: The TrafficLight class uses time to manage its state (green, yellow, red). Cars manage their direction, speed, and turn_decision.

*Collision Detection: Demonstrates basic collision detection by checking if a car's "sensor" pygame.Rect collides with another car's rect.

*2D Animation: Creates the illusion of movement by updating the x and y coordinates of each car's rect every frame and redrawing it.

## 📄 License

A second year CGV project by Soujanya Shanbhag.

Distributed under the MIT License.
