# Popis Algoritmu pro Vizualizaci Fraktálů

## Úvod

Tento kód implementuje interaktivní vizualizér fraktálů v Pythonu s použitím knihoven NumPy a Matplotlib. Umožňuje uživateli prozkoumávat Mandelbrotovu a Juliovu množinu s různými parametry a vizuálními nastaveními.

## Klíčové Komponenty

### Třída `FractalVisualizer`

Hlavní třída, která zajišťuje celou funkcionalitu programu. Obsahuje:

- Inicializaci parametrů (výchozí hodnoty pro vykreslení, nastavení zobrazení)
- Uživatelské rozhraní s posuvníky, tlačítky a textovými poli
- Funkce pro výpočet fraktálů
- Funkce pro interakci s uživatelem

### Algoritmy pro Výpočet Fraktálů

1. **Mandelbrotova množina**:
   - Iterativní proces používající vzorec z(n+1) = z(n)² + c
   - Pro každý bod komplexní roviny (c) se testuje, zda posloupnost z(0) = 0 diverguje
   - Výsledná barva závisí na počtu iterací potřebných k překročení prahové hodnoty

2. **Juliova množina**:
   - Podobný princip jako Mandelbrotova množina
   - Konstantní hodnota c je fixní pro celou množinu
   - Každý bod komplexní roviny je počáteční hodnotou z iterace

### Interakce s Uživatelem

- **Zoom**: Levé tlačítko myši pro přiblížení, pravé pro oddálení
- **Posuvník**: Nastavení počtu iterací
- **Přepínače**: Výběr typu fraktálu a barevné mapy
- **Textová pole**: Zadání konstanty c pro Juliovu množinu
- **Tlačítka**: Reset zoomu, export obrázku

## Matematické Principy

Kód využívá principů komplexní analýzy a teorie chaosu. Fraktály jsou generovány sledováním chování komplexních čísel v iterativním procesu. Pro každý bod se zaznamenává, jak rychle hodnota iterace překročí určitou mez (v tomto případě 2).

## Efektivita a Optimalizace

Kód zahrnuje jednoduchou optimalizaci výkonu - při velkém přiblížení se automaticky snižuje rozlišení, aby se zachovala plynulost aplikace.

## Návrhy na Vylepšení

1. **Paralelizace výpočtů**: Implementace pomocí `multiprocessing` nebo `numba` by mohla výrazně zrychlit generování fraktálů, což by bylo užitečné při vysokém rozlišení nebo velkém počtu iterací.

2. **Možnost ukládání a načítání zajímavých míst**: Přidání funkcionality pro uložení souřadnic zajímavých oblastí a možnost se k nim později vrátit.

3. **Rozšíření nabídky fraktálů**: Přidání dalších typů fraktálů jako Burning Ship, Newton nebo Lyapunov.
