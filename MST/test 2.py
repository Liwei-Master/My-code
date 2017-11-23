import math
import random
import heapq

priority_queue = [2,3,4,5,6,7,1,8,9,10]


def heapfy(priority_queue, index):
    old_index = index
    is_modified = False
    max_index = priority_queue.__len__()
    while index * 2 + 1 < max_index:

        if priority_queue[index] > priority_queue[index * 2 + 1]:
            internal = priority_queue[index * 2 + 1]
            priority_queue[index * 2 + 1] = priority_queue[index]
            priority_queue[index] = internal
            is_modified = True

        if (index * 2 + 2) != max_index:
            if priority_queue[index] > priority_queue[index * 2 + 2]:
                internal = priority_queue[index * 2 + 2]
                priority_queue[index * 2 + 2] = priority_queue[index]
                priority_queue[index] = internal
                index = index * 2 + 2
                is_modified = True
            else:
                index = index * 2 + 1
        else:
            index = index * 2 + 1

    if is_modified == False:
        while old_index >= 0:

            if priority_queue[old_index] < priority_queue[int((old_index - 1) / 2)]:
                internal = priority_queue[int((old_index - 1) / 2)]
                priority_queue[int((old_index - 1) / 2)] = priority_queue[old_index]
                priority_queue[old_index] = internal
                old_index = int((old_index - 1) / 2)
            else:
                old_index = -1
    return priority_queue

print(heapfy(priority_queue, 6))