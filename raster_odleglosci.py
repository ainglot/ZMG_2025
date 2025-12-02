import numpy as np

def distance_from_center(shape, pixel_size=1.0):
    """
    shape: (rows, cols) - rozmiar rastra
    pixel_size: rozdzielczość przestrzenna (np. 10 m/piksel)
    """
    rows, cols = shape

    # Indeksy wierszy i kolumn
    y_idx, x_idx = np.indices((rows, cols))

    # Środek rastra (może być niecałkowity przy parzystych wymiarach)
    cy = (rows - 1) / 2.0
    cx = (cols - 1) / 2.0

    # Różnice w jednostkach pikseli
    dy = (y_idx - cy) * pixel_size
    dx = (x_idx - cx) * pixel_size

    # Odległość euklidesowa od środka
    dist = np.hypot(dx, dy)  # to samo co np.sqrt(dx**2 + dy**2)

    return dist

# Przykład użycia:
dist_mat = distance_from_center((5, 5), pixel_size=10)
print(dist_mat)
