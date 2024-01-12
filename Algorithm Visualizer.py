import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import threading
import time

class SortVisualizer:
    def __init__(self, root, array_size=10):
        self.root = root
        self.root.configure(bg='#2D2D2D')
        self.root.set_theme('yaru')  # Set the theme
        self.root.configure(bg='#2D2D2D')
        self.array_size = array_size
        self.array = list(range(1, self.array_size+1))
        random.shuffle(self.array)
        self.sorting = False
        self.delay = 0.1  # Initial delay time in seconds
        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0

        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.fig.patch.set_facecolor('black')
        self.plot = self.fig.add_subplot(111)
        self.plot.set_facecolor('#2D2D2D')
        self.plot.spines['bottom'].set_color('#E0E0E0')
        self.plot.spines['top'].set_color('#E0E0E0') 
        self.plot.spines['right'].set_color('#E0E0E0')
        self.plot.spines['left'].set_color('#E0E0E0')
        self.plot.xaxis.label.set_color('#E0E0E0')
        self.plot.yaxis.label.set_color('#E0E0E0')
        self.plot.tick_params(axis='x', colors='#E0E0E0')
        self.plot.tick_params(axis='y', colors='#E0E0E0')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root) 
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.button_frame = tk.Frame(self.root, bg='#2D2D2D')
        self.button_frame.pack(side=tk.BOTTOM)

        style = ttk.Style(self.root)  # Create a style object
        style.configure('TButton', background='#2D2D2D', foreground='#E0E0E0')  # Configure the style of the button
        style.configure('TLabel', background='#2D2D2D', foreground='#E0E0E0')  # Configure the style of the label

        self.button_frame = ttk.Frame(self.root)  # Use ttk Frame
        self.button_frame.pack(side=tk.BOTTOM)

        self.shuffle_button = tk.Button(self.button_frame, text='Shuffle', command=self.shuffle, fg='black', bg='#2D2D2D')
        self.shuffle_button.pack(side=tk.LEFT)

        self.sort_button = tk.Button(self.button_frame, text='Sort', command=self.sort, fg='black', bg='#2D2D2D')
        self.sort_button.pack(side=tk.LEFT)

        self.cancel_button = tk.Button(self.button_frame, text='Cancel', command=self.cancel_sort, fg='black', bg='#2D2D2D')
        self.cancel_button.pack(side=tk.LEFT)

        self.array_size_var = tk.StringVar(self.button_frame)
        self.array_size_var.set("10") 

        self.array_size_option = tk.OptionMenu(self.button_frame, self.array_size_var, "10", "20", "50", "100")
        self.array_size_option.config(bg='#2D2D2D', fg='#E0E0E0')
        self.array_size_option["menu"].config(bg='black', fg='white')
        self.array_size_option.pack(side=tk.RIGHT)

        self.algorithm_var = tk.StringVar(self.button_frame)
        self.algorithm_var.set("Bubble Sort") 

        self.algorithm_option = tk.OptionMenu(self.button_frame, self.algorithm_var, "Bubble Sort", "Selection Sort", "Insertion Sort", "Quick Sort", "Heap Sort")
        self.algorithm_option.config(bg='#2D2D2D', fg='#E0E0E0')
        self.algorithm_option["menu"].config(bg='black', fg='white')
        self.algorithm_option.pack(side=tk.RIGHT)

        self.speed_slider = tk.Scale(self.button_frame, from_=1, to=100, orient=tk.HORIZONTAL, label='Speed', length=200, command=self.update_delay, bg='black', fg='white', troughcolor='grey')
        self.speed_slider.pack(side=tk.RIGHT)
        self.speed_slider.set(10)  # Default speed setting

        self.algorithm_info = tk.Label(self.root, text="", bg='black', fg='white')
        self.algorithm_info.pack(side=tk.BOTTOM, fill=tk.BOTH)

        self.metrics_label = tk.Label(self.root, text="", bg='black', fg='white')
        self.metrics_label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_delay(self, value):
        self.delay = 1 / float(value)

    def update_plot(self, array, swap1=None, swap2=None):
        self.plot.clear()
        color_array = ['blue']*len(array)
        if swap1 or swap1==0:
            color_array[swap1] = 'red'
        if swap2 or swap2==0:
            color_array[swap2] = 'red'
        self.plot.bar(range(len(array)), array, color=color_array)
        self.canvas.draw()
        self.sort_button.config(state='normal')  # Enable 'Sort' button after update
        time.sleep(self.delay)# Add delay for visualization
        self.metrics_label.config(text=f"Time: {time.time() - self.start_time:.3f} s, Comparisons: {self.comparisons}, Swaps: {self.swaps}")  

    def shuffle(self):
        self.array_size = int(self.array_size_var.get())
        self.array = list(range(1, self.array_size+1))
        random.shuffle(self.array)
        self.update_plot(self.array)
        self.comparisons = 0
        self.swaps = 0
        self.metrics_label.config(text=f"Time: 0 s, Comparisons: 0, Swaps: 0")

    def bubble_sort(self, array):
        n = len(array)
        for i in range(n):
            if not self.sorting: break
            for j in range(0, n-i-1):
                if not self.sorting: break
                self.comparisons += 1
                if array[j] > array[j+1] :
                    array[j], array[j+1] = array[j+1], array[j]
                    self.swaps += 1
                    self.update_plot(array, j, j+1)
        if self.sorting:
            self.shuffle_button.config(state='normal')

    def selection_sort(self, array):
        for i in range(len(array)):
            if not self.sorting: break
            min_idx = i
            for j in range(i+1, len(array)):
                if not self.sorting: break
                self.comparisons += 1
                if array[j] < array[min_idx]:
                    min_idx = j
            array[i], array[min_idx] = array[min_idx], array[i]
            self.swaps += 1
            self.update_plot(array, i, min_idx)
        if self.sorting:
            self.shuffle_button.config(state='normal')

    def insertion_sort(self, array):
        for i in range(1, len(array)):
            if not self.sorting: break
            key = array[i]
            j = i-1
            while j >= 0 and key < array[j] :
                if not self.sorting: break
                array[j+1] = array[j]
                j -= 1
                self.comparisons += 1
            array[j+1] = key
            self.swaps += 1
            self.update_plot(array, j, i)
        if self.sorting:
            self.shuffle_button.config(state='normal')

    def quick_sort(self, array, low, high):
        if not self.sorting: return
        if low < high:
            pi = self.partition(array, low, high)
            self.quick_sort(array, low, pi-1)
            self.quick_sort(array, pi+1, high)
            self.update_plot(array)
        if low == 0 and high == len(array) - 1 and self.sorting:
            self.shuffle_button.config(state='normal')

    def partition(self, array, low, high):
        i = (low-1)
        pivot = array[high]
        for j in range(low, high):
            if not self.sorting: break
            self.comparisons += 1
            if array[j] < pivot:
                i = i+1
                array[i], array[j] = array[j], array[i]
                self.swaps += 1
                self.update_plot(array, i, j)
        array[i+1], array[high] = array[high], array[i+1]
        self.swaps += 1
        return (i+1)

    def heapify(self, array, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and array[i] < array[l]:
            largest = l
        if r < n and array[largest] < array[r]:
            largest = r
        if largest != i:
            array[i],array[largest] = array[largest],array[i]
            self.swaps += 1
            if self.sorting:  # Check whether sorting has been cancelled
                self.heapify(array, n, largest)
                self.update_plot(array, i, largest)


    def heap_sort(self, array):
        n = len(array)
        for i in range(n//2 - 1, -1, -1):
            if self.sorting:  # Check whether sorting has been cancelled
                self.comparisons += 1
                self.heapify(array, n, i)
        for i in range(n-1, 0, -1):
            if self.sorting:  # Check whether sorting has been cancelled
                array[i], array[0] = array[0], array[i]
                self.comparisons += 1
                self.heapify(array, i, 0)
                self.update_plot(array, i, 0)
        if self.sorting:
            self.shuffle_button.config(state='normal')


    def sort(self):
        self.sort_button.config(state='disabled')  # Disable 'Sort' button during sorting
        self.shuffle_button.config(state='disabled')  # Disable 'Shuffle' button during sorting
        self.sorting = True
        self.start_time = time.time()
        algorithm = self.algorithm_var.get()
        algorithm = self.algorithm_var.get()
        algorithm_info_dict = {"Bubble Sort": "Bubble Sort: O(n^2). Bubble sort is the simplest sorting algorithm that works by repeatedly swapping the adjacent elements if they are in wrong order.",
                               "Selection Sort": "Selection Sort: O(n^2). The selection sort algorithm sorts an array by repeatedly finding the minimum element from unsorted part and putting it at the beginning.",
                               "Insertion Sort": "Insertion Sort: O(n^2). The insertion sort algorithm that builds final sorted array one item at a time. It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort.",
                               "Quick Sort": "Quick Sort: O(nlogn). Quick sort is an efficient sorting algorithm, serving as a systematic method for placing the elements of a random access file or an array in order.",
                               "Heap Sort": "Heap Sort: O(nlogn). Heap sort is a comparison based sorting technique based on Binary Heap data structure."}
        self.algorithm_info.config(text=algorithm_info_dict[algorithm])
        if algorithm == "Bubble Sort":
            threading.Thread(target=self.bubble_sort, args=(self.array,)).start()
        elif algorithm == "Selection Sort":
            threading.Thread(target=self.selection_sort, args=(self.array,)).start()
        elif algorithm == "Insertion Sort":
            threading.Thread(target=self.insertion_sort, args=(self.array,)).start()
        elif algorithm == "Quick Sort":
            threading.Thread(target=self.quick_sort, args=(self.array, 0, len(self.array)-1)).start()
        elif algorithm == "Heap Sort":
            threading.Thread(target=self.heap_sort, args=(self.array,)).start()


    def cancel_sort(self):
        self.sorting = False
        self.shuffle_button.config(state='normal')  # Enable 'Shuffle' button after cancel


if __name__ == "__main__":
    root = ThemedTk(theme="yaru")  # Create a ThemedTk window
    root.geometry('500x500')
    SortVisualizer(root)
    root.mainloop()