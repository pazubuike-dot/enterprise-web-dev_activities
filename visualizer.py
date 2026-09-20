import time
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import random

def time_complexity_visualizer(algorithm, n_min, n_max, step):
    times = []
    input_sizes = list(range(n_min, n_max + 1, step))

    plt.ion() 
    fig, ax = plt.subplots()
    ax.set_xlabel('input size')
    ax.set_ylabel('Running time (seconds)')
    ax.set_title('Algorithm time complexity visualization (Live)')
    line, = ax.plot([], [], '-o')

    for i, n in enumerate(input_sizes):
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)

        line.set_data(input_sizes[:i + 1], times)
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.01)

    plt.ioff()
    
    # Save the plot locally so your Flask app can grab it later!
    plt.savefig('complexity_plot.png')
    
    plt.show()

def linear_search(n):
    arr = np.random.randint(0, 100000, size=n)
    target = np.random.randint(0, 100000)
    for i in range(n):
        if arr[i] == target:
            return i
    return -1

def bubble_sort(n):
    arr = [random.randint(0, 1000) for _ in range(n)]
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def binary_search(n):
    arr = sorted([random.randint(0, 100000) for _ in range(n)])
    target = random.randint(0, 100000)
    low, high = 0, n - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def nested_loops(n):
    counter = 0
    for i in range(n):
        for j in range(n):
            counter += 1
    return counter