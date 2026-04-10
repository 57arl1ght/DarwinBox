import pygame
import pymunk
import pymunk.pygame_util
import copy
import random
from creature import Creature

def clear_space(space):
    """Removes all bodies and springs from the world except the floor and obstacles"""
    for c in list(space.constraints):
        space.remove(c)
    for s in list(space.shapes):
        
        if s.body.body_type != pymunk.Body.STATIC:
            space.remove(s)
    for b in list(space.bodies):
        if b.body_type != pymunk.Body.STATIC:
            space.remove(b)

def main():
    pygame.init()
    width, height = 1000, 600
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    font = pygame.font.SysFont("Arial", 28, bold=True)

    space = pymunk.Space()
    space.gravity = (0, 900)

    
    floor = pymunk.Segment(space.static_body, (-1000, height - 50), (10000, height - 50), 10)
    floor.friction = 1.0
    floor.elasticity = 0.3
    space.add(floor)

  
    for x in range(400, 5000, 250):
        block_w = 20
        block_h = random.randint(15, 35)
        
        block_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        block_body.position = (x, height - 50 - block_h/2)
        block_shape = pymunk.Poly.create_box(block_body, (block_w, block_h))
        block_shape.friction = 1.0
        block_shape.color = (120, 120, 120, 255) 
        space.add(block_body, block_shape)

    pop_size = 15 
    creatures = []
    
    for i in range(pop_size):
        creatures.append(Creature(space, 100, 400))

    generation = 1
    gen_time = 0.0
    max_gen_time = 25.0 

    running = True
    time = 0.0

    print("🧬 DarwinBox: Obstacle course activated!")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = 1/60.0
        time += dt * 3 
        gen_time += dt

        for c in creatures:
            c.update(time)

       
        if gen_time >= max_gen_time:
            creatures.sort(key=lambda c: c.get_fitness(), reverse=True)
            winners = creatures[:3]
            
            new_record = winners[0].get_fitness()
            
            
            if 'last_best_fitness' not in locals(): last_best_fitness = 0
            if 'stagnation_counter' not in locals(): stagnation_counter = 0

            if abs(new_record - last_best_fitness) < 1.0:
                stagnation_counter += 1
            else:
                stagnation_counter = 0
                last_best_fitness = new_record

            print(f"Покоління {generation} | Рекорд: {new_record:.1f} px | Застій: {stagnation_counter}")

            clear_space(space)
            new_creatures = []
            
            
            m_power = 6.0 if stagnation_counter > 5 else 1.0
            if stagnation_counter > 5: print("⚠️ GENETIC STORM ACTIVATED!")

            # ЕЛІТИЗМ
            new_creatures.append(Creature(space, 100, 400, copy.deepcopy(winners[0].dna), mutate=False))
            
            
            while len(new_creatures) < pop_size:
                parent1, parent2 = random.sample(winners, 2)
                child_dna = copy.deepcopy(parent1.dna)
                new_creatures.append(Creature(space, 100, 400, child_dna, mutate=m_power))
                
            creatures = new_creatures
            generation += 1
            gen_time = 0
            time = 0 

        
        screen.fill((230, 240, 250)) 
        space.debug_draw(draw_options) 
        
        text_gen = font.render(f"Generation: {generation}", True, (50, 50, 50))
        text_time = font.render(f"Time to Judgment Day: {max_gen_time - gen_time:.1f} s", True, (200, 50, 50))
        screen.blit(text_gen, (20, 20))
        screen.blit(text_time, (20, 60))

        space.step(dt) 
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()