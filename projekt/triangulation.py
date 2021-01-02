import numpy as np


# Funkcja sprawdzająca, czy dwa odcinki są tą samą krawędzią.
def is_shared(edge1, edge2):
    return edge1[0] == edge2[0] and edge1[1] == edge2[1] \
           or edge1[0] == edge2[1] and edge1[1] == edge2[0]


# Funkcja zwracająca krawędzie utworzone z wierzchołków w kolejności przeciwnej do ruchu wskazówek zegara.
def make_cww(a, b, c):
    val = (float(b.y - a.y) * (c.x - b.x)) - \
            (float(b.x - a.x) * (c.y - b.y))
    if val < 0:
        return [[a, b],
                [b, c],
                [c, a]]
    else:
        return [[b, a],
                [a, c],
                [c, b]]


# Struktura opisująca punkt.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Funkcja sprawdzająca czy dany punkt znajduje się wewnątrz okręgu opisanego na trójkącie.
    def is_inside(self, triangle):
        p1 = triangle.a
        p2 = triangle.b
        p3 = triangle.c
        p4 = self

        # Wyliczamy wyznacznik poniżej macierzy, jeśli jest on większy od zera, to ten punkt znajduje się
        # wewnątrz okręgu opisanego na danym trójkącie.
        matrix = np.array([[p1.x - p4.x, p1.y - p4.y, (p1.x - p4.x) ** 2 + (p1.y - p4.y) ** 2],
                           [p2.x - p4.x, p2.y - p4.y, (p2.x - p4.x) ** 2 + (p2.y - p4.y) ** 2],
                           [p3.x - p4.x, p3.y - p4.y, (p3.x - p4.x) ** 2 + (p3.y - p4.y) ** 2]])

        return np.linalg.det(matrix) > 0


# Struktura opisująca trójkąt.
class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.edges = make_cww(a, b, c)
        self.neighbour = [[-1]] * 3

    # Funkcja sprawdzająca czy dany punkt jest wierzchołkiem tego trójkąta.
    def has_vertex(self, point):
        return self.a == point or self.b == point or self.c == point


# Główna struktura algorytmu.
class DelaunayTriangulation:
    def __init__(self, width, height):
        # Lista przechowująca odcinki triangulacji.
        self.triangulation = []

        # Wierzchołki supertrójkąta.
        self.SuperPointA = Point(-100, -100)
        self.SuperPointB = Point(2 * width + 100, -100)
        self.SuperPointC = Point(-100, 2 * height + 100)

        # Tworzenie trójkąta i dodanie go do triangulacji.
        super_triangle = Triangle(self.SuperPointA, self.SuperPointB, self.SuperPointC)
        self.triangulation.append(super_triangle)

    # Główna funkcja struktury, dodająca punkt do obecnej triangulacji, zachowując jej poprawność.
    def add_point(self, point):
        bad_triangles = []

        # Sprawdzamy czy dany punkt znajduje się wewnątrz okręgu opisanego na trójkątach obecnych w triangulacji.
        # Jeśli tak, to dodajemy go to listy "złych" trójkątów.
        for triangle in self.triangulation:
            if point.is_inside(triangle):
                bad_triangles.append(triangle)

        # Chęcią usunięcia złych trójkątów z triangulacji powstał wielokąt, na którym należy dokonać triangulacji.
        # W poniższej pętli szukamy otoczki wypukłej znalezionych złych trójkątów.
        # Jest to nasz wielokąt - lista przechowująca krawędzie.
        polygon = []

        # Sprawdzamy każdą krawędź należącą do złych trójkątów i porównujemy ją z każdą inną.
        # Jest to podejście nieco czasochłonne, ale bardzo proste w implementacji.
        for triangle in bad_triangles:
            for edge in triangle.edges:
                is_neighbour = False
                for other in bad_triangles:
                    if triangle == other:
                        continue
                    for other_edge in other.edges:
                        if is_shared(edge, other_edge):
                            # Jeśli krawędź jest wspólna dla dwóch trójkątów, to nie dodajemy jej do wielokąta.
                            is_neighbour = True
                if not is_neighbour:
                    polygon.append(edge)

        # W końcu możemy rzeczywiście usunąć złe trójkąty.
        for triangle in bad_triangles:
            self.triangulation.remove(triangle)

        # Uzyskany wielokąt triangulujemy, czyli łączymy aktualnie przetwarzany punkt z wierzchołkami wielokąta.
        for edge in polygon:
            triangle = Triangle(edge[0], edge[1], point)
            self.triangulation.append(triangle)

    # Funkcja usuwająca supertrójkąt za pomocą funkcji lambda.
    def remove_super_triangles(self):
        for triangle in self.triangulation[:]:
            on_super = triangle.has_vertex(self.SuperPointA) \
                       or triangle.has_vertex(self.SuperPointB) \
                       or triangle.has_vertex(self.SuperPointC)
            if on_super is True:
                self.triangulation.remove(triangle)

    # Funkcja znajdująca sąsiadów dla każdego trójkąta z triangulacji.
    def find_neighbours(self):
        # Każdy trójkąt porównujemy z każdym innym z triangulacji, dlatego też ta metoda jest czasochłonna.
        # Sąsiedzi przechowywani są w trzyelementowej liście.
        # Jeśli dana krawędź jest wspólna, to pod danym indeksem przechowywana jest lista zawierająca dany trójkąt
        # oraz wspólną krawędź.
        # Jeśli dana krawędź nie posiada sąsiada, to znaczy że jest ona krawędzią zewnętrzną. Taka sytuacja jest
        # oznaczana jako [-1], inicjacja przebiega podczas tworzenia struktury trójkąta.
        for triangle in self.triangulation:
            _edge = -1
            for edge in triangle.edges:
                _edge += 1
                for other in self.triangulation:
                    if triangle == other:
                        continue
                    for other_edge in other.edges:
                        if is_shared(edge, other_edge):
                            triangle.neighbour[_edge] = [other]
                            triangle.neighbour[_edge].append(edge)

    # Funkcja zwracająca krawędzie uzyskanej triangulacji.
    def export_edges(self):
        edges = []
        for triangle in self.triangulation:
            for edge in triangle.edges:
                edges.append(([edge[0].x, edge[0].y], [edge[1].x, edge[1].y]))
        return edges

    # Funkcja zachowująca się jak silnik.
    # Po kolei dodaje punkty do triangulacji a następnie usuwa supertrójkąt, szuka sąsiadów
    # oraz zwraca listę krawędzi przeprowadzonej triangulacji.
    def run(self, pts):
        for point in pts:
            p = Point(point[0], point[1])
            self.add_point(p)
        self.remove_super_triangles()
        self.find_neighbours()
        return self.export_edges()
