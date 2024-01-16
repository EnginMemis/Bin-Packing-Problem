import copy
import random
from BLF import BottomLeftFill
from shapes import *
class GA():
    def __init__(self, bin_width, bin_height, poly_list, generations, pop_size):
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.poly_list = poly_list
        self.generations = generations
        self.pop_size = pop_size
        self.pop = []
        self.pop_index = []
        self.population = []
        self.mutate_rate = 0.3
        self.mutate_size = 0.1
        self.elite_size = 5

    def getIndex(self, poly_list):
        index_list = []
        for rect in poly_list:
            index_list.append(rect.index)
        return index_list

    def calculateDensity(self, shapes_list):
        bin = Bin(self.bin_width, self.bin_height)
        blf = BottomLeftFill(bin, shapes_list)
        blf.place()
        return blf
    
    def mutate(self, index_list, shapes_list):
        
        if random.random() <= self.mutate_rate:
            for _ in range(int(len(shapes_list) * self.mutate_size)):
                index1 = random.randint(0, len(index_list) - 1)
                index2 = random.randint(0, len(index_list) - 1)
                index_list[index1], index_list[index2] = index_list[index2], index_list[index1]
                shapes_list[index1], shapes_list[index2] = shapes_list[index2], shapes_list[index1]

        else:
            for _ in range(int(len(shapes_list) * self.mutate_size)):
                index = random.randint(0, len(index_list) - 1)
                index = 0
                shapes_list[index].rotate()

        return index_list, shapes_list

    def crossover(self, parent1, parent2):
        geneA,geneB = random.randint(0,len(parent1)-1), random.randint(0,len(parent1)-1)
        start_gene,end_gene = min(geneA, geneB),max(geneA, geneB)
        child1 = parent1[start_gene:end_gene]
        child2 = [gen for gen in parent2 if gen not in child1]
        child = child1 + child2
        return child
        

    def genetic_algorithm(self):
        self.highest_density = 0.0
        self.highest_pop = []
        self.pop.append(self.poly_list)
        orig_index_list = self.getIndex(self.poly_list)
        self.pop_index.append(orig_index_list)

        blf = self.calculateDensity(self.poly_list)
        self.population.append((blf.density, self.poly_list, blf.bin))

        if blf.density > 0.999:
            return self.poly_list, blf.density, blf.bin
        
        #BUYUKTEN KUCUGE SIRALI

        sorted_list = copy.deepcopy(self.poly_list)
        sorted_list = sorted(sorted_list, key=lambda rect: (rect.width * rect.height), reverse=True)
        
        blf = self.calculateDensity(sorted_list)
        self.population.append((blf.density, sorted_list, blf.bin))

        if blf.density > 0.999:
            return sorted_list, blf.density, blf.bin
        
        #KUCUKTEN BUYUGE SIRALI
        
        sorted_list = copy.deepcopy(self.poly_list)
        sorted_list = sorted(sorted_list, key=lambda rect: (rect.width * rect.height))
        
        blf = self.calculateDensity(sorted_list)
        self.population.append((blf.density, sorted_list, blf.bin))

        if blf.density > 0.999:
            return sorted_list, blf.density, blf.bin

        #POPULASYON OLUSTURMA

        new_index_list = orig_index_list.copy()
        for _ in range(self.pop_size - 3):
            random.shuffle(new_index_list)
            pop_list = copy.deepcopy(self.poly_list)
            sorted_pairs = sorted(zip(new_index_list, pop_list))
            result_list = [pair[1] for pair in sorted_pairs]
            self.pop.append(result_list)
            self.pop_index.append(new_index_list)

            blf = self.calculateDensity(result_list)
            self.population.append((blf.density, result_list, blf.bin))

            if blf.density > 0.999:
                return result_list, blf.density, blf.bin
            
        
        #POPULASYONU BASARIYA GORE SIRALAMA VE GENERATIONS

        for generation_index in range(self.generations):

            self.population = sorted(self.population, key=lambda x: (x[0]), reverse=True)

            print(f"{generation_index} : {self.population[0][0]} - {self.population[1][0]} - {self.population[2][0]} - {self.population[3][0]}")

            new_population = []
            for i in range(self.elite_size):
                new_population.append(self.population[i])

            for i in range(self.pop_size - self.elite_size):
                index1 = random.randint(0, self.elite_size - 1)
                index2 = random.randint(0, self.elite_size - 1)

                child_index = self.crossover(self.pop_index[index1], self.pop_index[index2])
                pop_list = copy.deepcopy(self.poly_list)
                sorted_pairs = sorted(zip(child_index, pop_list))
                child_list = [pair[1] for pair in sorted_pairs]

                child_index, child_list = self.mutate(child_index, child_list)

                blf = self.calculateDensity(child_list)
                new_population.append((blf.density, child_list, blf.bin))

            self.population = new_population

        return self.population[0][1], self.population[0][0], self.population[0][2]

        
        