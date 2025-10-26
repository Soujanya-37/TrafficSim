import pygame
import random
import time

# --- Initialize Pygame ---
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Traffic Simulation")

# --- Colors ---
COLOR_BACKGROUND = (40, 40, 40)  # Dark grey
COLOR_ROAD = (100, 100, 100)     # Lighter grey
COLOR_STOP_LINE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLACK = (0, 0, 0)

# --- Road and Intersection Setup ---
ROAD_WIDTH = 100
INTERSECTION_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
# Define the road rectangles
ROAD_VERTICAL = pygame.Rect(INTERSECTION_CENTER[0] - ROAD_WIDTH // 2, 0, ROAD_WIDTH, SCREEN_HEIGHT)
ROAD_HORIZONTAL = pygame.Rect(0, INTERSECTION_CENTER[1] - ROAD_WIDTH // 2, SCREEN_WIDTH, ROAD_WIDTH)
# Define the stop lines for cars
STOP_LINE_V_TOP = INTERSECTION_CENTER[1] - ROAD_WIDTH // 2 - 10
STOP_LINE_V_BOTTOM = INTERSECTION_CENTER[1] + ROAD_WIDTH // 2 + 10
STOP_LINE_H_LEFT = INTERSECTION_CENTER[0] - ROAD_WIDTH // 2 - 10
STOP_LINE_H_RIGHT = INTERSECTION_CENTER[0] + ROAD_WIDTH // 2 + 10


# --- Traffic Light Class ---
class TrafficLight:
    """Manages the state of a single traffic light."""
    def __init__(self, direction):
        self.direction = direction  # 'vertical' or 'horizontal'
        self.state = 'green'
        self.last_change_time = time.time()
        self.cycle_time = {'green': 10, 'yellow': 2, 'red': 12} # Duration in seconds

        if self.direction == 'horizontal':
            # Horizontal starts as red to alternate with vertical
            self.state = 'red'

    def update(self):
        """Updates the light state based on the timer."""
        current_time = time.time()
        time_elapsed = current_time - self.last_change_time

        if self.state == 'green' and time_elapsed > self.cycle_time['green']:
            self.state = 'yellow'
            self.last_change_time = current_time
        elif self.state == 'yellow' and time_elapsed > self.cycle_time['yellow']:
            self.state = 'red'
            self.last_change_time = current_time
        elif self.state == 'red' and time_elapsed > self.cycle_time['red']:
            self.state = 'green'
            self.last_change_time = current_time

    def draw(self, screen):
        """Draws the traffic light on the screen."""
        # Simple representation: a colored square
        light_size = 20
        if self.direction == 'vertical':
            pos = (INTERSECTION_CENTER[0] + ROAD_WIDTH // 2 + 10, STOP_LINE_V_TOP - 30)
        else: # horizontal
            pos = (STOP_LINE_H_LEFT - 30, INTERSECTION_CENTER[1] - ROAD_WIDTH // 2 - 30)

        color = COLOR_BLACK
        if self.state == 'green':
            color = COLOR_GREEN
        elif self.state == 'yellow':
            color = COLOR_YELLOW
        elif self.state == 'red':
            color = COLOR_RED

        pygame.draw.rect(screen, color, (pos[0], pos[1], light_size, light_size))


# --- Car Class ---
class Car:
    """Manages the state and movement of a single car."""
    def __init__(self, direction):
        self.direction = direction
        self.width = 30
        self.height = 50
        self.speed = random.uniform(2, 4) # Give cars slightly different speeds
        # Pick a random color for the car
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        
        # --- New Features ---
        self.turn_decision = random.choice(['straight', 'right'])
        self.is_turning = False
        # --- End New Features ---

        # Set initial position based on direction
        if self.direction == 'north':
            self.rect = pygame.Rect(INTERSECTION_CENTER[0] + 5, SCREEN_HEIGHT + self.height, self.width, self.height)
        elif self.direction == 'south':
            self.rect = pygame.Rect(INTERSECTION_CENTER[0] - self.width - 5, -self.height, self.width, self.height)
        elif self.direction == 'east':
            self.rect = pygame.Rect(-self.width, INTERSECTION_CENTER[1] + 5, self.height, self.width) # Note: w/h swapped
        elif self.direction == 'west':
            self.rect = pygame.Rect(SCREEN_WIDTH + self.width, INTERSECTION_CENTER[1] - self.width - 5, self.height, self.width) # Note: w/h swapped

    def move(self, vertical_light, horizontal_light, all_cars):
        """Moves the car, checks for lights, and handles collisions/turning."""
        can_move = True

        # --- 1. Collision Detection ---
        # Check for other cars in front
        sensor_rect = self.rect.copy()
        detection_distance = int(self.speed * 1.5) # Look ahead based on speed
        
        if self.direction == 'north':
            sensor_rect.y -= detection_distance
        elif self.direction == 'south':
            sensor_rect.y += detection_distance
        elif self.direction == 'east':
            sensor_rect.x += detection_distance
        elif self.direction == 'west':
            sensor_rect.x -= detection_distance

        for other_car in all_cars:
            if other_car is not self and sensor_rect.colliderect(other_car.rect):
                # Check if they are in the same lane (same direction)
                if self.direction == other_car.direction:
                        can_move = False
                        break
        
        # --- 2. Traffic Light Check ---
        if self.direction == 'north':
            if (vertical_light.state == 'red' or vertical_light.state == 'yellow') and \
                self.rect.bottom > STOP_LINE_V_BOTTOM and self.rect.bottom < STOP_LINE_V_BOTTOM + 20:
                can_move = False
        
        elif self.direction == 'south':
            if (vertical_light.state == 'red' or vertical_light.state == 'yellow') and \
                self.rect.top < STOP_LINE_V_TOP and self.rect.top > STOP_LINE_V_TOP - 20:
                can_move = False

        elif self.direction == 'east':
            if (horizontal_light.state == 'red' or horizontal_light.state == 'yellow') and \
                self.rect.left < STOP_LINE_H_LEFT and self.rect.left > STOP_LINE_H_LEFT - 20:
                can_move = False
        
        elif self.direction == 'west':
            if (horizontal_light.state == 'red' or horizontal_light.state == 'yellow') and \
                self.rect.right > STOP_LINE_H_RIGHT and self.rect.right < STOP_LINE_H_RIGHT + 20:
                can_move = False

        # --- 3. Turning Logic ---
        # Check if car can and wants to turn right
        if self.turn_decision == 'right' and not self.is_turning and can_move:
            if self.direction == 'north' and self.rect.bottom < (INTERSECTION_CENTER[1] + ROAD_WIDTH // 2):
                self.is_turning = True
                self.direction = 'west'
                self.rect.width, self.rect.height = self.rect.height, self.rect.width # Swap w/h
            elif self.direction == 'south' and self.rect.top > (INTERSECTION_CENTER[1] - ROAD_WIDTH // 2):
                self.is_turning = True
                self.direction = 'east'
                self.rect.width, self.rect.height = self.rect.height, self.rect.width
            elif self.direction == 'east' and self.rect.left > (INTERSECTION_CENTER[0] - ROAD_WIDTH // 2):
                self.is_turning = True
                self.direction = 'north'
                self.rect.width, self.rect.height = self.rect.height, self.rect.width
            elif self.direction == 'west' and self.rect.right < (INTERSECTION_CENTER[0] + ROAD_WIDTH // 2):
                self.is_turning = True
                self.direction = 'south'
                self.rect.width, self.rect.height = self.rect.height, self.rect.width

        # --- 4. Final Movement ---
        if can_move:
            if self.direction == 'north':
                self.rect.y -= self.speed
            elif self.direction == 'south':
                self.rect.y += self.speed
            elif self.direction == 'east':
                self.rect.x += self.speed
            elif self.direction == 'west':
                self.rect.x -= self.speed

    def draw(self, screen):
        """Draws the car on the screen."""
        pygame.draw.rect(screen, self.color, self.rect)


# --- Main Game Loop ---
def main():
    running = True
    clock = pygame.time.Clock()

    # Create traffic lights
    light_vertical = TrafficLight('vertical')
    light_horizontal = TrafficLight('horizontal')
    
    cars = []
    last_spawn_time = time.time()
    spawn_delay = 1 # Spawn a new car every N seconds

    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Game State Update ---
        
        # Update traffic lights
        light_vertical.update()
        light_horizontal.update()

        # Spawn new cars periodically
        current_time = time.time()
        if current_time - last_spawn_time > spawn_delay:
            direction = random.choice(['north', 'south', 'east', 'west'])
            cars.append(Car(direction))
            last_spawn_time = current_time
            # Add some randomness to spawn delay
            spawn_delay = random.uniform(1, 3) 

        # Move cars
        for car in cars:
            car.move(light_vertical, light_horizontal, cars)

        # Remove cars that are off-screen
        cars = [car for car in cars if 
                car.rect.bottom > -50 and 
                car.rect.top < SCREEN_HEIGHT + 50 and 
                car.rect.right > -50 and 
                car.rect.left < SCREEN_WIDTH + 50]

        # --- Drawing ---
        
        # Draw background
        SCREEN.fill(COLOR_BACKGROUND)
        
        # Draw roads
        pygame.draw.rect(SCREEN, COLOR_ROAD, ROAD_VERTICAL)
        pygame.draw.rect(SCREEN, COLOR_ROAD, ROAD_HORIZONTAL)

        # Draw stop lines
        pygame.draw.line(SCREEN, COLOR_STOP_LINE, (ROAD_VERTICAL.left, STOP_LINE_V_TOP), (ROAD_VERTICAL.right, STOP_LINE_V_TOP), 3)
        pygame.draw.line(SCREEN, COLOR_STOP_LINE, (ROAD_VERTICAL.left, STOP_LINE_V_BOTTOM), (ROAD_VERTICAL.right, STOP_LINE_V_BOTTOM), 3)
        pygame.draw.line(SCREEN, COLOR_STOP_LINE, (STOP_LINE_H_LEFT, ROAD_HORIZONTAL.top), (STOP_LINE_H_LEFT, ROAD_HORIZONTAL.bottom), 3)
        pygame.draw.line(SCREEN, COLOR_STOP_LINE, (STOP_LINE_H_RIGHT, ROAD_HORIZONTAL.top), (STOP_LINE_H_RIGHT, ROAD_HORIZONTAL.bottom), 3)

        # Draw traffic lights
        light_vertical.draw(SCREEN)
        light_horizontal.draw(SCREEN)

        # Draw cars
        for car in cars:
            car.draw(SCREEN)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60) # Aim for 60 frames per second

    pygame.quit()

# --- Run the main function ---
if __name__ == "__main__":
    main()

