# RankingMethod
### Filip Tłuszcz, Wojciech Ciężobka
Aplikacja z interfejsem graficznym licząca wielokryterialny i wieloekspertowy ranking AHP.

## Funkcjonalności
* wyznaczanie rankingu AHP zarówno metodą wektorów włąsnych (EVM) jak i metodą średniej geometrycznej (GMM).
* Liczenie rankingów wielokryterialnych
* Zbieranie danych od wielu ekspertó i wyznaczenie wspólnego rankingu. Realizujemy ten punkt na dwa sposoby:
  * Poprzez agregacje osobistych osądów (AIJ), gdzie na początku agregujemy macierze porównań a następnie wyliczmy ranking
  * Poprzez agregacje osobistych priorytetów (AIP), gdzie najpierw wyliczamy osobne rankingi dla każdego eksperta, a na końcu agregujemy rankingi do finalnego pojedyńczego rankingu
* Wsparcie dla weryfikacji niespójności. Dla metody GMM wyliczany jest *geometryczny indeks niespójności* (GCI), z kolei dla metody EVM wyliczany jest zarówno *indeks niespójności Saaty-Harker* jak i *consistency ratio*

## Architektura aplikacji
Python + JS itd itp

## Pierwsze uruchomienie
### Wymagania
* *python 3.x* wraz z biblioteką *numpy* 
* *node.js* (wersja 16 lub wyższa)
### Uruchomienie
1. Należy sklonować powyższe repozytorium ```git clone https://github.com/Tluszczyk/RankingMethod.git```
2. Z poziomu katalogu ```RankingMethod``` wywołać komendę ```node app```
3. W lini komend pojawi informacja z linkiem jak poniżej lub podobnym: \
```Application started and Listening on port http://localhost:3000 or on some other environmental port``` \
Należy wejść w link i przejść do podpunktu **Opis użycia**

## Opis użycia
Aplikację możemy stosować w celu wyznaczenia rankingu metodą AHP. Aby to zrobić wystarczy uruchomić aplikację (jak opisano w punkcie powyżej). Aplikacja w przeglądarce wyświetli ekran startowy, z poziomu którego możemy określić kryteria rankingu, alternatywy, liczbę ekspertów biorących udział w ocenie oraz metodę, którą zostanie wyliczony ranking. Po zatwierdzeniu wszystkich parametrów, aplikacja przeniesie nas przez kolejne zestawy macierzy porównań, które musimy wypełnić (w całości lub nie), aby otrzymać ranking. Po zatwierdzeniu każdej z macierzy, otrzymamy informację o jej niespójności, i możemy albo przejść dalej, albo poprawić nasze odpowiedzi. Na samym końcu, gdy system zbierze wszystkie potrzebne porównania, otrzymamy informację zwrotną ze znormalizowanym rankingiem końcowym.

## Sprawozdanie z części I Projektu
https://docs.google.com/document/d/16-jIBeoELckmhWv2ocsNaJHDrKQYotKbcjiHpBtg8DI/edit?usp=sharing
