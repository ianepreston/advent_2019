import numpy as np

IN = "day_08/input.txt"
EX = "day_08/example.txt"
EX2 = "day_08/example2.txt"


def linereader(file, width, height):
    with open(file, "r") as f:
        return np.array([int(char) for char in f.readline().rstrip()]).reshape(
            (-1, height, width)
        )


def pixel_counter(array):
    layer = np.argmax(np.count_nonzero(array, axis=(1, 2)))
    array_layer = array[layer]
    ones = (array_layer == 1).sum()
    twos = (array_layer == 2).sum()
    return ones * twos


EX_RES = pixel_counter(linereader(EX, 3, 2))
assert EX_RES == 1
IN_RES = pixel_counter(linereader(IN, 25, 6))
print(IN_RES)


def layer_pixels(array):
    for i in range(array.shape[0] - 1, 0, -1):
        mask = array[i - 1] == 2
        array[i - 1, mask] = array[i, mask]
    return array[0]


assert (layer_pixels(linereader(EX2, 2, 2)) == np.array([[0, 1], [1, 0]])).all()

print(layer_pixels(linereader(IN, 25, 6)))
