import time

  # bubble sort
  
def bubble_sort(data):
    arr = data.copy()
    comparisons = 0
    swaps = 0

    start = time.perf_counter()

    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            comparisons += 1

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1

    end = time.perf_counter()

    return {
        "sorted_data": arr,
        "time_ms": (end - start) * 1000,
        "comparisons": comparisons,
        "swaps": swaps,
        "complexity": "O(n^2)",
        "stable": "Yes"
    }
  # insertion sort

def insertion_sort(data):
    arr = data.copy()
    comparisons = 0
    swaps = 0

    start = time.perf_counter()

    for i in range(1, len(arr)):
        j = i

        while j > 0:
            comparisons += 1

            if arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                swaps += 1
                j -= 1
            else:
                break

    end = time.perf_counter()

    return {
        "sorted_data": arr,
        "time_ms": (end - start) * 1000,
        "comparisons": comparisons,
        "swaps": swaps,
        "complexity": "O(n^2)",
        "stable": "Yes"
    }
   # selection sort

def selection_sort(data):
    arr = data.copy()
    comparisons = 0
    swaps = 0

    start = time.perf_counter()

    for i in range(len(arr)):
        min_index = i

        for j in range(i + 1, len(arr)):
            comparisons += 1

            if arr[j] < arr[min_index]:
                min_index = j

        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            swaps += 1

    end = time.perf_counter()

    return {
        "sorted_data": arr,
        "time_ms": (end - start) * 1000,
        "comparisons": comparisons,
        "swaps": swaps,
        "complexity": "O(n^2)",
        "stable": "No"
    }

  # merge sort
def merge_sort(data):
    arr = data.copy()
    comparisons = 0
    swaps = 0

    start = time.perf_counter()

    def sort(arr):
        nonlocal comparisons, swaps

        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2

        left = sort(arr[:mid])
        right = sort(arr[mid:])

        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            comparisons += 1

            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
                

        result.extend(left[i:])
        result.extend(right[j:])

        return result

    arr = sort(arr)

    end = time.perf_counter()

    return {
        "sorted_data": arr,
        "time_ms": (end - start) * 1000,
        "comparisons": comparisons,
        "swaps": swaps,
        "complexity": "O(n log n)",
        "stable": "Yes"
    }

  # hybrid merge sort

def hybrid_merge_sort(data):
    arr = data.copy()
    comparisons = 0
    swaps = 0

    start = time.perf_counter()

    def sort(arr):
        nonlocal comparisons, swaps

        if len(arr) <= 10:
            for i in range(1, len(arr)):
                j = i

                while j > 0:
                    comparisons += 1

                    if arr[j] < arr[j - 1]:
                        arr[j], arr[j - 1] = arr[j - 1], arr[j]
                        swaps += 1
                        j -= 1
                    else:
                        break

            return arr

        mid = len(arr) // 2

        left = sort(arr[:mid])
        right = sort(arr[mid:])

        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            comparisons += 1

            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result

    arr = sort(arr)

    end = time.perf_counter()

    return {
        "sorted_data": arr,
        "time_ms": (end - start) * 1000,
        "comparisons": comparisons,
        "swaps": swaps,
        "complexity": "O(n log n)",
        "stable": "Yes"
    }

   # quick sort
def quick_sort(data):
    arr = data.copy()
    comparisons = 0
    swaps = 0

    start = time.perf_counter()

    def sort(arr):
        nonlocal comparisons, swaps

        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]

        left = []
        middle = []
        right = []

        for x in arr:
            comparisons += 1

            if x < pivot:
                left.append(x)
            elif x == pivot:
                middle.append(x)
            else:
                right.append(x)

        return sort(left) + middle + sort(right)

    arr = sort(arr)

    end = time.perf_counter()

    return {
        "sorted_data": arr,
        "time_ms": (end - start) * 1000,
        "comparisons": comparisons,
        "swaps": swaps,
        "complexity": "O(n log n) average",
        "stable": "Yes"
    }

   # heap sort
def heap_sort(data):
    arr = data.copy()
    comparisons = 0
    swaps = 0

    start = time.perf_counter()

    def heapify(n, i):
        nonlocal comparisons, swaps

        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n:
            comparisons += 1
            if arr[left] > arr[largest]:
                largest = left

        if right < n:
            comparisons += 1
            if arr[right] > arr[largest]:
                largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            swaps += 1
            heapify(n, largest)

    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        swaps += 1
        heapify(i, 0)

    end = time.perf_counter()

    return {
        "sorted_data": arr,
        "time_ms": (end - start) * 1000,
        "comparisons": comparisons,
        "swaps": swaps,
        "complexity": "O(n log n)",
        "stable": "No"
    }
