DarwinBox: Genetic Evolution Simulation
DarwinBox is a 2D evolution simulation where virtual creatures learn to navigate an obstacle course using genetic algorithms. Starting from random movements, creatures evolve their physical structure and muscle coordination to overcome increasingly difficult terrain.

🚀 Key Features
Pymunk Physics Engine: Realistic simulation of rigid bodies, circular nodes, and damped spring muscles.

Genetic Algorithm: Implementation of natural selection, crossover, and mutation strategies.

Dynamic Morphology: Creatures can "grow" new nodes or "prune" unnecessary parts of their bodies during evolution to find the most efficient shape.

Genetic Storm (Anti-Stagnation): A unique system that automatically increases mutation power (radiation level) when the population hits an evolutionary plateau.

Contextual Fitness Function: An advanced scoring system that rewards horizontal speed on flat ground and switches to vertical "climbing" bonuses when obstacles are detected.

🛠 Tech Stack
Python 3.x

Pygame — for real-time visualization.

Pymunk — for 2D physics calculations.

📈 Evolutionary Milestones
During testing, the population successfully evolved from chaotic "vibrating masses" into specialized "climbers":

Early Generations: 60-100 px (struggling to move).

Current Record: 1600+ px, successfully clearing multiple vertical walls.

💻 Installation & Usage
Install the required dependencies:

Bash
pip install pygame pymunk
Run the simulation:

Bash
python main.py

⚙️ How It Works
Each creature possesses a unique DNA string that encodes the number of nodes, their spatial offsets, and muscle parameters (speed, amplitude, and rest length).

Generation Cycle: Every 25 seconds, the top 3 performers are selected as "parents."

Mutation: Random structural and behavioral changes are applied to the offspring.

Pruning: The system encourages minimalism by occasionally removing nodes, preventing "over-complicated" but inefficient bodies.
