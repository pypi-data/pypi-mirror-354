def bubbleSort(lst: list) -> list:
    made_a_swap = True

    while made_a_swap:
        made_a_swap = False
        for i in range(len(lst) - 1):
            if lst[i] > lst[i+1]:
                made_a_swap = True
                temp = lst[i]
                lst[i] = lst[i+1]
                lst[i+1] = temp
    return lst

# def test_bubble_sort():
#     assert bubbleSort([]) == []
#     assert bubbleSort([42]) == [42]
#     assert bubbleSort([1, 2, 3]) == [1, 2, 3]
#     assert bubbleSort([3, 2, 1]) == [1, 2, 3]
#     assert bubbleSort([4, 2, 5, 2, 3]) == [2, 2, 3, 4, 5]
#     assert bubbleSort([-3, -1, -2, 0, 2]) == [-3, -2, -1, 0, 2]
#     assert bubbleSort([3, -2, 1, -5, 0]) == [-5, -2, 0, 1, 3]
#     assert bubbleSort([1, 1, 1, 1]) == [1, 1, 1, 1]
#     assert bubbleSort([1000000, 500000, -1000000]) == [-1000000, 500000, 1000000]
#     assert bubbleSort([1.2, 3.4, 0.5, 2.2]) == [0.5, 1.2, 2.2, 3.4]

#     print("All test cases passed!")

# test_bubble_sort()
