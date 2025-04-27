# L-System Generátor

## Popis programu
Aplikace pro generování a vizualizaci L-systémů pomocí jazyka Python a knihovny Tkinter. Program umožňuje vytvářet, upravovat a zkoumat fraktální struktury založené na L-systémech.

## Co jsou L-systémy?

L-systémy (Lindenmayerovy systémy) jsou formální gramatiky, které se používají k modelování růstu rostlin a různých fraktálních struktur. Každý L-systém se skládá z:
- **Axiomu**: počáteční řetězec symbolů
- **Pravidel přepisu**: instrukce, jak nahradit každý symbol v řetězci
- **Interpretace**: jak převést výsledný řetězec na grafickou reprezentaci

## Funkce programu

Program nabízí následující funkce:
- Generování fraktálů založených na L-systémech
- Přednastavené typy fraktálů (Koch Snowflake, Koch Curve, Plant, Bush)
- Možnost definovat vlastní axiomy a pravidla přepisu
- Nastavení úhlu otáčení, počtu iterací a délky čáry
- Nastavení počáteční pozice a orientace
- Přibližování, oddalování a posouvání vygenerovaného fraktálu
- Barevné zobrazení fraktálu pro lepší vizualizaci hloubky či struktury

## Implementace

Program je rozdělen do dvou tříd:

### 1. LSystemFractal
Třída se stará o logiku L-systémů:
- Zpracování axiomu a pravidel přepisu
- Generování výsledného řetězce po definovaném počtu iterací
- Vykreslování fraktálu na plátno

### 2. App
Vytváří grafické uživatelské rozhraní:
- Inicializace okna aplikace s tmavým tématem
- Vytvoření ovládacích prvků (vstupní pole, tlačítka)
- Zpracování událostí uživatelského rozhraní (kliknutí, tažení)
- Implementace funkcionality přiblížení a posunu
- Správa přednastavených L-systémů

## Algoritmus generování L-systémů

Generování L-systému probíhá ve dvou fázích:

1. **Generování řetězce**:
   - Začínáme s axiomem
   - V každé iteraci procházíme aktuální řetězec znak po znaku
   - Každý znak nahradíme podle pravidel přepisu (nebo ponecháme, pokud nemá pravidlo)
   - Po dokončení všech iterací máme výsledný řetězec

2. **Vykreslování řetězce**:
   - Začínáme na definované pozici s definovaným směrem
   - Procházíme výsledný řetězec znak po znaku
   - Interpretujeme každý znak:
     - 'F': Pohyb vpřed s kreslením čáry
     - 'b': Pohyb vpřed bez kreslení
     - '+': Otočení doprava o definovaný úhel
     - '-': Otočení doleva o definovaný úhel
     - '[': Uložení aktuální pozice a směru na zásobník
     - ']': Obnovení poslední uložené pozice a směru ze zásobníku

## Možná vylepšení

Z hlediska budoucího rozvoje vidím několik možností pro vylepšení:
1. **Rozšíření sady symbolů** - přidání více symbolů pro komplexnější struktury
2. **Export obrázků** - možnost uložit vygenerovaný fraktál jako obrázek
3. **Více pravidel přepisu** - umožnit definovat více pravidel pro jeden L-systém
4. **Animace růstu** - vizualizace postupného růstu fraktálu po iteracích
5. **Optimalizace výkonu** - pro velmi složité L-systémy by mohla být užitečná optimalizace vykreslování
6. **3D L-systémy** - rozšíření na trojrozměrné L-systémy
7. **Ukládání L-Systémů** - rozšířit program o možnost perzistentního ukládání dalších fraktálů
