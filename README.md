# DelaunayVoronoi
Program przedstawiający diagram Voronoi z użyciem algorytmu opartego na triangulacji Delaunay.

Aby uruchomić program należy pobrać potrzebne pliki. W tym celu należy kliknąć zielony przycisk "Code" znajdujący się na górze po prawej stronie w stosunku do wyświetlanych plików a następnie kliknąć przycisk "Download ZIP". Pobrany folder należy rozpakować, plik "voronoi" otworzyć w IDE (np. PyCharm) i uruchomić.

Domyślnie przedstawiony jest diagram Voronoi dla 100 losowo rozmieszczonych punktów. Wizualizacja korzysta z biblioteki matplotlib i jest skontruowana w taki sposób, że początkowo widać wszystkie narysowane punkty - nawet te mało ważne. Aby wyraźniej zobaczyć diagram należy użyć lupki i przybliżyć obraz.
W wizualizacji nie zostały przedstawione półproste zmierzające w nieskończoność (jest to spowodowane niewłaściwym warunkiem wyznaczania punktu w nieskończoności). Wyjaśnienie tego problemu znajduje się w dokumentacji. Funkcja potrzebna do wizualizacji takich półprostych została zakomentowana.
