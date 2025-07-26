# The Reforger | ver_early_alpha

# Last update .alpha2607250
- dodano "[Fight]" do log_system.py
- poprawiono wyglad wyswietlania logów
- dodano obsługe krytycznego trafienia w player.py:
   *get_damage() - updated
   *roll_crit() - new
- dodano plik README


Autor: devansk

## Opis

The Reforger to tekstowy RPG w Pythonie, rozwijany w stylu klasycznych gier singleplayer. Projekt jest w fazie wczesnej alphy i stale rozwijany.

## Zawartość projektu

### 🔶 🧙 Klasa Player
- Ekwipunek
- Statystyki: HP, obrona, atak, crit, monety
- Zdobywanie doświadczenia (XP)
- Levelowanie postaci (LVL)
- Obsługa walki (fight.py)
- Zapis/odczyt stanu gracza i ekwipunku

#### Do dodania
- [NIEDAWNO DODANE] Obsługa crit podczas zwracania player.damage
- Bardziej złożony system doświadczenia
- Umiejętności do walki / pasywne do zbierania
- Speed attack do statystyk

---

### 🔶 👾 Klasa Monster
- Statystyki: HP, obrona, atak, XP, drop, drop_rate (d_chance)
- Obsługa walki (fight.py)
- Losowanie przeciwnika (resources/monsters.py)
- Drop itemów po śmierci (resources/drop.py)

#### Do dodania
- Uaktualnić funkcję drop o szanse na drop z danego przedmiotu (item.drop_chance)
- Level up po 20 zabójstwach + atak, + hp + obrona +xp (milestones)
- Licznik śmierci danej bestii
---

### 🔶 🎒 Klasa Inventory
- Dodawanie/usuwanie przedmiotów
- Obsługa quantity do m_quantity (max stack 1-32)
- Zapis/odczyt z pliku
- Obsługa sklepu (kupno/sprzedaż) [BRAK]

#### Do dodania
- Stackowanie po przekroczeniu m_quantity
- Usuwanie po id i ilości
- Wyrzucanie/sprzedawanie itemów
- Ekwipunek na sobie (bonusy do statystyk)

---

### 🔶 🏺 Klasa Items
- Obsługuje wszystkie przedmioty (weapons, shields, potions, drop)
- Dodatkowe funkcje (np. leczenie dla potions)
- Odczyt z plików (resources/drop, potions, weapons, shields)

#### Do dodania
- Rozszerzyć dodatkowe funkcje
- Dodać więcej przedmiotów i typów

---

### 🔶 🏺 Klasa Fight
- Walka gracz vs potwór
- Drop przedmiotów
- Reset XP po śmierci gracza
- Dodawanie XP po zabiciu przeciwnika

#### Do dodania
- Bardziej zaawansowany system walki
- Możliwość ucieczki

---

## Uruchomienie

1. Sklonuj repozytorium:
   ```bash
   git clone <adres_repo>
   ```
2. Uruchom `main.py` w Pythonie 3.10+.

## Wymagania
- Python 3.10+

## Plany rozwoju
- Rozbudowa ekwipunku i systemu walki
- Nowe typy przedmiotów i potworów
- System umiejętności i statusów
- Integracja z plikami JSON (save/load)

---

Projekt w fazie ALPHA – kod i mechaniki mogą się zmieniać!
