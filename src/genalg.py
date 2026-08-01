import copy
import random as rand
from bird import Bird
from settings import POPULATION_SIZE

def ranked_select(pool, ct=3):
    samp = rand.sample(pool,ct)
    return max(samp, key=lambda bird: bird.fitness)

def next_gen(birds):
    birds.sort(key=lambda bird: bird.fitness, reverse=True)

    new_pop = []

    for i in range(5):
        best_brain = copy.deepcopy(birds[i].brain)
        new_pop.append(Bird(brain=best_brain))

    top_parents = birds[:30]
    while len(new_pop) < POPULATION_SIZE:
        parent = ranked_select(top_parents, ct=3)
        child_brain = copy.deepcopy(parent.brain)
        child_brain.mutate()
        new_pop.append(Bird(brain=child_brain))
    return new_pop