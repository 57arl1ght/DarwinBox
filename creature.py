import pymunk
import random
import math
import pygame

def create_node(space, x, y):
    body = pymunk.Body(0.5, 50)
    body.position = x, y
    shape = pymunk.Circle(body, 12)
    shape.friction = 1.2
    shape.elasticity = 0.5
    shape.filter = pymunk.ShapeFilter(group=1) 
    shape.color = pygame.Color(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
    space.add(body, shape)
    return body

class Creature:
    def __init__(self, space, start_x, start_y, dna=None, mutate=True):
        self.nodes = []
        self.muscles = []
        self.start_x = start_x
        
        m_power = mutate if isinstance(mutate, (int, float)) else 1.0
        
        if dna is None:
            num_nodes = 3 
            self.dna = {"num_nodes": num_nodes, "nodes_offsets": [], "muscles": []}
            for _ in range(num_nodes):
                dx, dy = random.randint(-30, 30), random.randint(-30, 30)
                self.dna["nodes_offsets"].append((dx, dy))
            
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    self.dna["muscles"].append(self.generate_muscle_dna(i, j))
        else:
            self.dna = dna

        # --- МУТАЦІЯ СТРУКТУРИ ---
        if mutate:
            # 1. Додавання вузла (як було)
            struct_mutation_chance = 0.05 * m_power
            if random.random() < struct_mutation_chance: 
                new_idx = self.dna["num_nodes"]
                self.dna["num_nodes"] += 1
                parent_node = random.choice(self.dna["nodes_offsets"])
                new_offset = (parent_node[0] + random.randint(-20, 20), parent_node[1] + random.randint(-20, 20))
                self.dna["nodes_offsets"].append(new_offset)
                
                targets = random.sample(range(new_idx), min(2, new_idx))
                for target_idx in targets:
                    self.dna["muscles"].append(self.generate_muscle_dna(target_idx, new_idx))

            # 2. ВИДАЛЕННЯ вузла (Нова логіка "чистки")
            # Шанс видалення вузла — 2%, але він зростає під час шторму
            if random.random() < (3 * m_power) and self.dna["num_nodes"] > 3:
                del_idx = random.randint(0, self.dna["num_nodes"] - 1)
                
                # Видаляємо офсет
                self.dna["nodes_offsets"].pop(del_idx)
                self.dna["num_nodes"] -= 1
                
                # Видаляємо всі м'язи, підключені до цього вузла
                self.dna["muscles"] = [m for m in self.dna["muscles"] if m["i"] != del_idx and m["j"] != del_idx]
                
                # Перераховуємо індекси вузлів у м'язах, що залишилися
                for m in self.dna["muscles"]:
                    if m["i"] > del_idx: m["i"] -= 1
                    if m["j"] > del_idx: m["j"] -= 1

        # Побудова фізичного тіла
        for dx, dy in self.dna["nodes_offsets"]:
            self.nodes.append(create_node(space, start_x + dx, start_y + dy))

        for m_dna in self.dna["muscles"]:
            if mutate:
                if random.random() < (0.2 * m_power): 
                    m_dna["speed"] += random.uniform(-1.0, 1.0) * m_power
                if random.random() < (0.2 * m_power): 
                    m_dna["amplitude"] += random.uniform(-4.0, 4.0) * m_power
                
                m_dna["speed"] = max(0.5, min(15, m_dna["speed"]))
                m_dna["amplitude"] = max(2, min(60, m_dna["amplitude"]))

            muscle = pymunk.DampedSpring(
                self.nodes[m_dna["i"]], self.nodes[m_dna["j"]], (0,0), (0,0),
                rest_length=m_dna["base_length"], stiffness=180, damping=10
            )
            space.add(muscle)
            self.muscles.append({"spring": muscle, "dna": m_dna})

    def generate_muscle_dna(self, i, j):
        return {
            "i": i, "j": j,
            "base_length": random.randint(30, 70),
            "speed": random.uniform(2.0, 8.0),
            "amplitude": random.uniform(10.0, 35.0)
        }

    def update(self, time):
        for m in self.muscles:
            dna = m["dna"]
            m["spring"].rest_length = dna["base_length"] + math.sin(time * dna["speed"]) * dna["amplitude"]
            
    def get_fitness(self):
        if not self.nodes: return 0
        
        # Позиції всіх вузлів по X
        all_x = [n.position.x for n in self.nodes]
        avg_x = sum(all_x) / len(all_x)
        avg_y = sum(n.position.y for n in self.nodes) / len(self.nodes)
        
        dist = avg_x - self.start_x
        
        # --- НОВА ЛОГІКА: ШТРАФ ЗА "ПОТЯГ" ---
        # Рахуємо довжину істоти (різниця між самим переднім і самим заднім вузлом)
        body_length = max(all_x) - min(all_x)
        
        # Якщо вони довші за 120 пікселів — починаємо віднімати бали
        length_penalty = 0
        if body_length > 120:
            length_penalty = (body_length - 120) * 0.5

        wall_threshold = 250.0 
        
        if dist > wall_threshold:
            # Чим вище вони над підлогою (550), тим краще
            height_bonus = (550 - avg_y) * 5.0 
            return dist + height_bonus - length_penalty
        else:
            return dist - length_penalty