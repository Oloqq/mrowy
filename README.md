# Zastosowanie algorytmu mrówkowego do wyznaczania optymalnej trasy na kampusie agh

### Autorzy:
- Olgierd Piofczyk
- Jakub Truszkowski
- Kinga Wrona

### Opis projeku:
Celem projektu jest wykorzystanie algorytmu mrówkowego do wyznaczenia optymalnej trasy przejścia po kampusie Akademii Górniczo-Hutniczej. 

Projekt wykorzystuje zasadę działania kolektywnej inteligencji kolonii mrówek, które w naturze znajdują najkrótsze ścieżki do pożywienia. 

Dzięki algorytmowi mrówkowemu sztuczne „mrówki” będą mogły symulować proces wyboru najlepszych tras, dostosowując swoje ścieżki na podstawie informacji o odwiedzonych miejscach i naniesionych śladach feromonowych.

## Uruchomienie programu:
Aby uruchomić program należy sklonować repozytorium, a następnie zainstalować wymagane biblioteki i uruchomić plik main.py

Zalecana wersja pythona: 3.11
```bash
pip install -r requirements.txt  
python main.py
```

## Sterowanie i rozpoczęcie symulacji:
Po uruchomieniu aplikacji widzimy testową mapę, która posłuży nam do zademonstrowania działania algorytmu mrówkowego.

### Cel i miejsce startu:
Aby dało się rozpocząc symulację należy wybrać miejsce startu, z którego mrówki zaczną swoją wędrówkę. Następnie należy wybrać cel podróży.

Aby to zrobić należy:
1. Kliknąć klawisz "s" na klawiaturze (umożliwi to stworzenie "gniazda")
2. Kliknąć na mapie miejsce startu
3. Kliknąć klawisz "t" na klawiaturze (umożliwi to stworzenie miejsca docelowego)
4. Kliknąć na mapie miejsce docelowe

### Rozpoczęcie symulacji:
Następnie aby uruchomić symulcję należy kliknąć klawisz "space" na klawiaturze. Jeżeli chcemy zmienić miejsce startu lub docelowe w każdej chwili można zatrzymać symulację klawiszem "space" i wykonać kroki 1-4 ponownie.

### Widok feromonów:
Aby wyświetlić widok feromonów należy kliknąć klawisz "f" na klawiaturze. Widok ten pozwala na zobaczenie śladu feromonowego pozostawionego przez mrówki.

## Mapa kampusu AGH:
Mapa kampusu AGH została stworzona na podstawie zdjęcia satelitarnego. Na mapie znajdują się budynki, trawniki oraz ścieżki, po których będą przemieszczać się studenci.

Akualnie algorytm, ze względów opymalizacyjnych, działa jedynie na mapach o mniejszych rozmiarach.

Docelowa mapa znajduję się w folderze "assets" w pliku "mapav4.png"