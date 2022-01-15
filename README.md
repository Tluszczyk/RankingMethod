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

## Architektura Aplikacji
## Instalacja - Pierwsze uruchomienie
### Wymagania
* *python 3.x* wraz z biblioteką *numpy* 
* *node.js* (wersja 16 lub wyższa)
1. Należy sklonować powyższe repozytorium\
```ala```
2. Z poziomu katalogu ```RankingMethod``` wywołać komendę ```node app```

## Sprawozdanie z części I Projektu
https://docs.google.com/document/d/16-jIBeoELckmhWv2ocsNaJHDrKQYotKbcjiHpBtg8DI/edit?usp=sharing
