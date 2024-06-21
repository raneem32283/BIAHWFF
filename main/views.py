from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render , redirect
from django.http import JsonResponse
from collections import defaultdict
import random
import numpy as np
from .models import City
from .models import Box
from .models import Car
def index(request):
    weight=0
    value=0
    destination_id=0
    weight_of_trak=0
    capacity=0
    if request.method == 'POST':
        if 'clear_data' in request.POST:
            Car.objects.all().delete()
            Box.objects.all().delete()
            return redirect('index')
        if 'weight' in request.POST and 'value' in request.POST:
            weight = request.POST.get('weight')
            value = request.POST.get('value')
            destination_id = request.POST.get('destination')
            # destination_id = City.objects.get(name=city_name)
            Box(weight=weight,value=value,destination_id=destination_id).save(False)
        if 'weight_of_trak' in request.POST:
            weight_of_trak = request.POST.get('weight_of_trak')
            capacity = request.POST.get('weight_of_trak')
            Car(weight_of_trak=weight_of_trak,capacity=capacity).save(True)
    cities = City.objects.all()
    boxes = Box.objects.all()
    cars = Car.objects.all()
    return render(request, 'pages/index.html', {'cities': cities, 'boxes': boxes, 'cars': cars})

car_capacity=[]
num_cars=0
boxes=[]
box=[]
weight_of_trak=0
cars_items=[]
cars_boxes=[]
def distance(city1,city2):
    distance_between_cities=np.linalg.norm(np.array(city1)-np.array(city2))
    return distance_between_cities
def initialize_population(population_size,number_of_boxes,number_of_cars):
    population=[]
    for i in range(population_size):
        individual=[random.randint(0,number_of_cars-1) for j in range(number_of_boxes)]
        population.append(individual)
    return population
def fitness(individual,boxes,cars_number,cities,car_capacity):
    total=0
    total_distance_car=[0] * cars_number
    car_loads=[0] * cars_number
    distance_betwen_cities=[0] * cars_number
    for i,car in enumerate(individual):
        car_loads[car]+=boxes[i][0]
        if car_loads[car] > car_capacity[car]:
            return 0
        total += boxes[i][1]
        total_distance_car[car]+=distance(cities[0],cities[boxes[i][2]])
        distance_betwen_cities[car] += distance(cities[boxes[i-1][2]], cities[boxes[i][2]])
    total_distance = sum(total_distance_car)
    total_distance_cities = sum(distance_betwen_cities)
    fitness_value=(total / (total_distance*max(total_distance_car)/total_distance_cities) if total_distance > 0 else 0)
    return fitness_value
def selection(population,fitnesses):
    index=np.random.choice(len(population),size=len(population),p=[fitnes/sum(fitnesses)for fitnes in fitnesses])
    return [population[i] for i in index]



def crossover(father,mother):
    size=len(father)
    start,end=sorted(random.sample(range(size),2))
    child=father[:start]+mother[start:end]+father[end:]
    return child

def mutate(individual,number_of_cars,mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i]=random.randint(0,number_of_cars-1)
    return individual
def genetic_algorithm(boxes, cars, cities, car_capacity, population_size, elite_size, mutation_rate, generations):
    num_boxes = len(boxes)
    population = initialize_population(population_size, num_boxes, cars)
    for _ in range(generations):
        fitnesses = [fitness(ind, boxes, cars, cities, car_capacity) for ind in population]
        population = selection(population, fitnesses)
        next_population = population[:elite_size]
        for _ in range(len(population) - elite_size):
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2)
            next_population.append(mutate(child, cars, mutation_rate))
        population = next_population
    best_individual = max(population, key=lambda ind: fitness(ind, boxes, cars, cities, car_capacity))
    return best_individual


# خوارزمية البائع المتجول
memo = None
path = None

def tsp(cities, n):
    global memo, path
    dist = [[distance(cities[i], cities[j]) for j in range(n)] for i in range(n)]
    memo = [[-1] * (1 << n) for _ in range(n)]
    path = [[None] * (1 << n) for _ in range(n)]

    def fun(i, mask):
        if mask == (1 << i) | 1:
            return dist[0][i], [0, i]
        
        if memo[i][mask] != -1:
            return memo[i][mask], path[i][mask]
        
        res = 10**9
        res_path = []
        
        for j in range(n):
            if (mask & (1 << j)) and j != i and j != 0:
                cost, sub_path = fun(j, mask & (~(1 << i)))
                cost += dist[j][i]
                if cost < res:
                    res = cost
                    res_path = sub_path + [i]
        
        memo[i][mask] = res
        path[i][mask] = res_path
        return res, res_path

    ans = 10**9
    final_path = []
    for i in range(1, n):
        cost, res_path = fun(i, (1 << n) - 1)
        cost += dist[i][0]
        if cost < ans:
            ans = cost
            final_path = res_path + [0]
    
    return ans, final_path

# دمج الخوارزميتين
def calculate_optimal_routes_for_cars(car_destinations, cities):
    routes = []
    for destinations in car_destinations:
        if not destinations:
            routes.append((0, []))
            continue
        full_route = [0] + list(set(destinations))
        full_cities = [cities[city] for city in full_route]
        cost, route = tsp(full_cities, len(full_cities))
        mapped_route = [full_route[i] for i in route]
        routes.append((cost, mapped_route))
    return routes
def car_items(number_cars,boxes,individual):
    car_destinations = [[] for _ in range(number_cars)]
    for i, number_cars in enumerate(individual):
        car_destinations[number_cars].append(boxes[i][2])
    return car_destinations
def car_lod(car_boxes,boxes,cars_number,car_capacity):
    total=0
    car_loads=0
    for i,car in enumerate(car_boxes):
        car_loads+=boxes[car][0]
        total += boxes[car][1]
    return total,car_loads
    
# def calculate_sum(box_names):
#     return Box.objects.filter(id__in=box_names).aggregate(total_value=models.Sum('value'))['total_value']
def index(request):
    cities = [(0, 0), (1, 5), (5, 1), (10, 10), (-3, 7),(10, -1), (-2, -9)]
    #إعدادات السيارات
    
    car_capacity=[]
    car_capacity_array=[]
    cars=Car.objects.all()
    num_cars =len(cars)
    car_capacity=list(cars.values('weight_of_trak'))
    # car_capacity_array=np.array(car_capacity)
    for car in cars:
        weight_of_trak=car.weight_of_trak
        car_capacity_array.append((weight_of_trak))
    # boxes=[]
    boxes_array=[]
    boxes=Box.objects.all()
    num_boxes=len(boxes)
    # boxes=list(boxes_all.values()) 
    # boxes_array=np.array(boxes)
    for box in boxes:
        weight=box.weight
        value=box.value
        city=box.destination_id
        boxes_array.append((weight, value, city))
    population_size = 100
    elite_size = 20
    mutation_rate = 0.01  # نسبة الطفرة
    generations = 1000 
    best_individual = genetic_algorithm(boxes_array, num_cars, cities, car_capacity_array, population_size, elite_size, mutation_rate, generations)
    # عرض النتائج
   # plt.plot([0, 0], [1, 5], [5, 1], [10, 10], [-3, 7],[10, -1], [-2, -9])
    #plt.ylabel('some numbers')
    #plt.show()
    # print("أفضل توزيع للصناديق على السيارات:", best_individual)
    best_fitness = fitness(best_individual, boxes_array, num_cars, cities, car_capacity_array)
    # print("الملاءمة لهذا التوزيع:", best_fitness)
    best_car_destinations = car_items(num_cars,boxes_array,best_individual)
    cities_to_visit=[]
    total=0
    for car_index, destinations in enumerate(best_car_destinations):
        cities_to_visit.append(destinations)
    value_indices=defaultdict(list)
    for index, value in enumerate(best_individual):
        value_indices[value].append(index)
    car_boxes = [value_indices[key] for key in sorted(value_indices.keys())]
    car_capacitys=[]
    car_total_value=[]
    car_total_weight=[]
    for car_value in car_boxes:
        car_capacityss,car_capacitys=car_lod(car_value,boxes_array,num_cars,car_capacity_array)
        car_total_value.append([car_capacityss])
        car_total_weight.append([car_capacitys])
    # for cars in car_boxes:
    #     for i in len(cars):
    #         car_size+=boxes_array[cars[i]][0]
    #     car_capacitys.append(car_size)
    # car_capacityss.append((car_capacitys))
    
    # car_loads=[0] * num_cars
    # for cars in car_boxes:
    #     for i,car in enumerate(cars):
    #         car_loads[car]+=boxes_array[i-1][0]
    #         total += boxes_array[i-1][1]
    #     car_capacityss.append(total)
    cars=[]
    for i in num_cars:
        cars.append([i])
    optimal_routes = calculate_optimal_routes_for_cars(best_car_destinations, cities)
    cities = City.objects.all()
    for car_index, (costs, route) in enumerate(optimal_routes):
        route.append([route])
        # cost.append([costs])
    all=list(cars.value(),car_boxes.value(),cities_to_visit.value(),best_fitness,car_total_value.value(),car_total_weight.value(),route.value())
    # print(f"الشاحنة {car_index + 1} ستزور المدن في المسار الأمثل: {route} بتكلفة {cost}")
    return render(request, 'pages/index.html', {'cities': cities, 'boxes': boxes, 'cars': cars,'all':all})