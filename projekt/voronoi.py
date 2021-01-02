import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt
from projekt.triangulation import DelaunayTriangulation


# Funkcja zwracająca współrzędne środka okręgu opisanego na danym trójkącie.
def circumctr(triangle):
    a = triangle.a
    b = triangle.b
    c = triangle.c

    D = 2 * (a.x*(b.y-c.y) + b.x*(c.y-a.y) + c.x*(a.y-b.y))
    U_x = 1/D * ((a.x**2 + a.y**2)*(b.y-c.y) + (b.x**2 + b.y**2)*(c.y-a.y) + (c.x**2 + c.y**2)*(a.y-b.y))
    U_y = 1/D * ((a.x**2 + a.y**2)*(c.x-b.x) + (b.x**2 + b.y**2)*(a.x-c.x) + (c.x**2 + c.y**2)*(b.x-a.x))

    return U_x, U_y


# Główna funkcja algorytmu. Wywołuje ona plik, gdzie znajduje się algorytm przeprowadzający triangulację i pobiera
# z niego listę krawędzi - trójkątów.
def voronoi(pts):
    # Domyślnie pracujemy na małych wartościach, dlatego też parametry width (szerokość) oraz height (wysokość)
    # są stosunkowo niewielkie.
    width = 100
    height = 100
    delaunay = DelaunayTriangulation(width, height)
    delaunay.run(pts)
    triangles = delaunay.triangulation

    segments = []  # Lista krawędzi przyszłego diagramu Voronoi.
    crcs_x = []    # Lista przechowująca współrzędne x środków okręgów - wizualizacja.
    crcs_y = []    # Lista przechowująca współrzędne y środków okręgów - wizualizacja.

    # Dla każdego trójkąta z triangulacji przeprowadzamy proces łączenia środka okręgu na nim opisanego
    # ze środkami okręgów jego sąsiadów, bądź z punktem znajdującym się blisko "nieskończoności"
    # dla zewnętrznych krawędzi.
    for i, triangle in enumerate(triangles):
        circumcenter = circumctr(triangle)
        for j, neighbor in enumerate(triangle.neighbour):
            # Jeśli dla danej krawędzi istnieje sąsiad:
            if triangle.neighbour[j][0] != -1:
                segments.append((circumcenter, circumctr(neighbor[0])))
                crcs_x.append([circumcenter[0]])
                crcs_y.append([circumcenter[1]])
            # Jeśli dla danej krawędzi nie istnieje sąsiad:
            else:
                # Szukamy tej krawędzi.
                edge = None
                for _edge in triangle.edges:
                    for neigh_edge in triangle.neighbour:
                        if neigh_edge == [-1]:
                            continue
                        if triangle.neighbour.count(_edge) == 0:
                            edge = _edge

                p1 = [edge[0].x, edge[0].y]
                p2 = [edge[1].x, edge[1].y]

                # Wyliczamy środek znalezionej krawędzi
                mid_x = 0.5 * (p1[0] + p2[0])
                mid_y = 0.5 * (p1[1] + p2[1])
                middle = np.array([mid_x, mid_y])

                # Szukamy wierzchołka trójkąta, który nie należy do znalezionej krawędzi.
                p3 = None
                if edge[0] != triangle.a and edge[1] != triangle.a:
                    p3 = triangle.a
                if edge[0] != triangle.b and edge[1] != triangle.b:
                    p3 = triangle.b
                if edge[0] != triangle.c and edge[1] != triangle.c:
                    p3 = triangle.c

                # Wyznaczami równanie prostej przechodzącej przez środek okręgu i środek znalezionej krawędzi.
                slope = (circumcenter[1] - middle[1]) / (circumcenter[0] - middle[0])
                x = 1000
                y = slope * (x - circumcenter[0]) + circumcenter[1]
                inf = np.array([x, y])

                # Wymyślony warunek wyznaczający czy półprosta dąży do +inf czy do -inf.
                # Jest on niepoprawny, wyjaśnienie w dokumentacji.
                val = (float(p2[0] - p1[0]) * (circumcenter[1] - p2[1])) - \
                      (float(p2[1] - p1[1]) * (circumcenter[0] - p1[0]))
                if val < 0:
                    x *= -1
                y = slope * (x - circumcenter[0]) + circumcenter[1]
                inf = np.array([x, y])

                # Dodanie środka okręgu obecnie przetwarzanego trójkąta do listy - wizualizacja.
                crcs_x.append([circumcenter[0]])
                crcs_y.append([circumcenter[1]])

                # Półproste idące w nieskończoność są czasem rysowane niepoprawnie, zasłaniając część diagramu.
                # Z tego powodu funkcja dodająca taką półprostą do diagramu została zakomentowana linijkę niżej.
                # segments.append((circumcenter, circumcenter + inf))

    # Zwracamy listę odcinków diagramu Voronoi praz punkty i krawędzie trójkątów podrzebne do wizualizacji.
    return segments, np.hstack((crcs_x, crcs_y)), delaunay.export_edges()


# Funkcja przechowująca dane punkty dla różnych zestawów danych.
def data_set(_type, size=100):
    circle_x = [[0.00041398571383567673], [-0.03573520783455142], [0.0013010824880292232], [0.03234946958480342],
                [0.016381727649319555], [0.02724866313319052], [0.03146237281060987], [0.03146237281060987],
                [0.027026888939642127], [0.0172688244235131], [-0.011118272350680448], [-0.022872304608744967],
                [-0.03307391751197077], [-0.031521498157132066], [-0.022206982028099807], [-0.012005369124874002]]
    circle_y = [[0.04873161867553115], [0.0022242657343546496], [-0.046642155834272815], [0.0012132363225899473],
                [0.04266544220494291], [0.02985906965592329], [0.015704657891217402], [-0.01631127348133163],
                [-0.0338357832852532], [-0.04327205779505713], [-0.04596813622642967], [-0.03552083230486104],
                [-0.01934436171662575], [0.02345588338141348], [0.040306373577491936], [0.04873161867553115]]

    line_x = [[-0.042166659447454645], [-0.032852143318422386], [-0.02331585299584174],
              [-0.01577553041519658], [-0.006904562673261089], [0.0021881792622227697],
              [0.011502695391255036], [0.021704308294480848], [0.03257124377835181], [0.04343817926222278]]
    line_y = [[0.044350491224550745], [0.03322916769513898], [0.02379289318533505],
              [0.015704657891217402], [0.007616422597099756], [-0.00013480289309632243],
              [-0.009234067598978685], [-0.01934436171662575], [-0.02810661661858653], [-0.03990195975584144]]

    rect_x = [[-0.05369891751197078], [0.05430511474609376], [0.05363979216544859], [-0.053920691705519164],
              [-0.04484271560544055], [-0.053894232215936456], [-0.05408681767573424], [-0.04696115566321618],
              [0.04547986503972076], [0.05395362527082331], [0.04547986503972076], [0.05433879619041887],
              [-0.035406028075349066], [-0.024813827786470878], [-0.014414212957390468], [-0.004592354507703414],
              [0.004844333022388056], [0.015436533311266251], [0.024873220841357735], [0.033924737451853634],
              [-0.039065151811506986], [-0.02962846428141551], [-0.01884367853273953], [-0.009792161922243622],
              [-0.00151098715093885], [0.006770187620365908], [0.016014289690659614], [0.025450977220751084],
              [0.034695079291044775], [-0.053894232215936456], [-0.053894232215936456], [-0.053894232215936456],
              [-0.05408681767573424], [0.05414621073062109], [0.05395362527082331], [0.05395362527082331],
              [0.05395362527082331]]
    rect_y = [[0.03996936377357037], [0.03862132455788407], [-0.04091298916760614], [-0.040238969559763006],
              [0.040311537529753236], [0.02706599541046649], [-0.028734373517592553], [-0.04028899536633205],
              [-0.04141627554669688], [-0.03098893387832221], [0.03918425734938842], [0.02706599541046649],
              [0.04002971748466204], [0.04002971748466204], [0.04002971748466204], [0.039747897439570815],
              [0.03918425734938842], [0.03918425734938842], [0.03946607739447962], [0.03946607739447962],
              [-0.04085263545651446], [-0.04057081541142325], [-0.04057081541142325], [-0.04085263545651446],
              [-0.04057081541142325], [-0.04057081541142325], [-0.04085263545651446], [-0.04085263545651446],
              [-0.04085263545651446], [0.015793193606818204], [0.005647671983534747], [-0.005906949865204764],
              [-0.01717975166885305], [0.015793193606818204], [0.005365851938443536], [-0.004497849639748724],
              [-0.01717975166885305]]

    triangle_x = [[-0.05347714331842239], [-0.052811820737777224], [0.04898253410093245], [-0.053474150835079434],
                  [-0.04639881704694962], [0.03786197624805088], [0.04129244111502291], [-0.053474150835079434],
                  [-0.0442547765050921], [-0.03610742244603353], [-0.028603280549532213], [-0.020027118382102138],
                  [-0.011450956214672063], [-0.004375622426542242], [0.003128519469959068], [0.011061469474831886],
                  [0.019423227588076214], [0.02842819786387779], [0.0346459154352646], [-0.053474150835079434],
                  [-0.053474150835079434], [-0.053474150835079434], [-0.053474150835079434], [-0.053474150835079434],
                  [-0.038680271096262556], [-0.02967530082046097], [-0.021099138653030897], [-0.011022148106300554],
                  [-0.001588369722127475], [0.0076310046078598565], [0.01620716677528994], [0.02606975326783452]]
    triangle_y = [[-0.03990195975584144], [0.03963235396964877], [-0.03956494995191987], [-0.029974379995900816],
                  [-0.04040172166427548], [-0.04011990161918427], [-0.033638040582086505], [0.030053289608526337],
                  [0.033153310104529626], [0.027235089157614273], [0.020753228120516498], [0.014553187128509934],
                  [0.0077895060463209626], [0.0021531051444968197], [-0.0040469358475097444], [-0.009401516704242677],
                  [-0.01560155769624924], [-0.022928878868620634], [-0.028001639680262362], [0.01934412789506046],
                  [0.0077895060463209626], [-0.002919655667144916], [-0.011656077064972334], [-0.020674318507890976],
                  [-0.04040172166427548], [-0.04040172166427548], [-0.04040172166427548], [-0.04040172166427548],
                  [-0.04011990161918427], [-0.04011990161918427], [-0.04040172166427548], [-0.03983808157409307]]

    # W zależności od przekazanego parametru "_type" zwracany jest odpowiedni zestaw danych.
    pts = {'random': np.random.random((size, 2)),
           'circle': np.hstack((circle_x, circle_y)),
           'line': np.hstack((line_x, line_y)),
           'rect': np.hstack((rect_x, rect_y)),
           'triangle': np.hstack((triangle_x, triangle_y))
           }[_type]
    return pts


def how_long(size = 300):
    P = np.random.random((size, 2))
    start = time.time()
    segments, x, y = voronoi(P)
    end = time.time()
    print(round(end - start, 4))


# Funkcja główna - main.
if __name__ == '__main__':
    # Zestawy danych do wyboru: 'random', 'circle', 'line', 'rect', 'triangle'.
    size = 100
    pts = data_set('triangle', size)

    # Wywołanie funkcji tworzącej diagram Voronoi.
    segments, crcs, triangles = voronoi(pts)

    # Dodanie potrzebnych punktów do wykresu.
    axes = plt.subplot(1, 1, 1)
    plt.scatter(pts[:, 0], pts[:, 1], marker='o')
    plt.scatter(crcs[:, 0], crcs[:, 1], color='r', marker=".")

    # Dodanie krawędzi trójkątów oraz krawędzi diagramu Voronoi do wykresu.
    lines = matplotlib.collections.LineCollection(segments, color='k')
    triangles = matplotlib.collections.LineCollection(triangles, color='g', linewidth=0.5)
    axes.add_collection(lines)
    axes.add_collection(triangles)

    # W przypadku zestawu losowych punktów poniższa linijka pomaga wycentrować diagram na wykresie.
    # plt.axis([-0.05, 1.05, -0.05, 1.05])

    plt.show()
