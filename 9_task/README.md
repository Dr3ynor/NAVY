# Analýza algoritmu pro generování fraktálních krajin

## Úvod

Tento dokument se zabývá implementací a analýzou algoritmu pro generování fraktálních krajin pomocí metody Diamond-Square. Implementace je realizovaná v jazyce Python s využitím knihoven NumPy pro matematické výpočty a MatPlotLib pro vizualizaci výsledků v 3D prostoru, s grafickým uživatelským rozhraním vytvořeným pomocí knihovny Tkinter.

## Princip algoritmu Diamond-Square

Diamond-Square algoritmus je rekurzivní metoda pro generování procedurálních výškových map, které vypadají přirozeně jako reálné krajiny. Jeho základním principem je postupné zjemňování mřížky s výškovými hodnotami přidáváním náhodných odchylek, přičemž velikost odchylek se s každou iterací zmenšuje.

### Matematický základ

Algoritmus pracuje s mřížkou o velikosti 2^n + 1 × 2^n + 1, kde n je počet iterací. To zajišťuje, že lze mřížku vždy rozdělit na poloviny při každé iteraci algortimu. 

Základní implementace obsahuje dvě hlavní fáze, které se opakují v každé iteraci:

1. **Diamond step**
2. **Square step**

### Detailní popis kroků algoritmu

#### Inicializace
- Vytvoří se matice (height_map) o velikosti (2^n + 1) × (2^n + 1)
- Inicializují se hodnoty v rozích matice (náhodné hodnoty z normálního rozdělení)

```python
self.height_map[0, 0] = np.random.normal(0, 1)
self.height_map[0, size] = np.random.normal(0, 1)
self.height_map[size, 0] = np.random.normal(0, 1)
self.height_map[size, size] = np.random.normal(0, 1)
```

#### Diamond step
V této fázi se pro každý čtverec v mřížce vypočítá hodnota jeho středu jako průměr hodnot ve čtyřech rozích čtverce plus náhodná odchylka:

$$h_{střed} = \frac{h_{levýHorní} + h_{pravýHorní} + h_{levýDolní} + h_{pravýDolní}}{4} + náhodná\_odchylka$$

V kódu implementováno jako:
```python
avg = (self.height_map[x, y] + 
       self.height_map[x + step, y] + 
       self.height_map[x, y + step] + 
       self.height_map[x + step, y + step]) / 4.0

self.height_map[x + half, y + half] = avg + np.random.normal(0, roughness)
```

#### Square step
V této fázi se vypočítají hodnoty středů každé hrany čtverce jako průměr dvou nebo více okolních bodů (podle toho, zda jde o hraniční body) plus náhodná odchylka:

$$h_{střed\_hrany} = \frac{\sum h_{okolní\_body}}{počet\_okolních\_bodů} + náhodná\_odchylka$$

Kód obsahuje logiku pro ošetření hraničních bodů mřížky, kde se průměruje jen z dostupných hodnot:
```python
avg = 0
count = 0
                    
if x >= half:
    avg += self.height_map[x - half, y]
    count += 1
if x + half < self.size:
    avg += self.height_map[x + half, y]
    count += 1
# ...další podmínky pro všechny směry...
                        
avg /= count
self.height_map[x, y] = avg + np.random.normal(0, roughness)
```

#### Rekurzivní dělení
Po dokončení Diamond a Square kroků se velikost kroku zmenší na polovinu:
```python
step = half
```

A zároveň se zmenší i velikost náhodné odchylky (roughness):
```python
roughness *= 0.5
```

Toto odpovídá matematicky persistenci (H):
$$roughness_{i+1} = roughness_i \cdot 2^{-H}$$

kde v tomto případě je implicitně H = 1, což dává:
$$roughness_{i+1} = roughness_i \cdot 0.5$$

## Vztah k fraktální geometrii

Výškové mapy generované Diamond-Square algoritmem vykazují fraktální vlastnosti - podobnost při různých měřítkách. Fraktální dimenze takto generovaného terénu závisí na faktoru zmenšování náhodnosti (roughness).

Statisticky vzato, pokud náhodnost klesá faktorem 0.5 s každou iterací, výsledný terén bude mít fraktální dimenzi přibližně D = 2.5, což realisticky odpovídá mnoha přírodním terénům.

## Implementační detaily

Program je implementován s dvěma hlavními třídami:
1. `FractalLandscape` - obsahuje samotný algoritmus generování
2. `FractalLandscapeApp` - obsahuje GUI a vizualizaci

### Třída FractalLandscape
- Inicializuje se s parametry pro počet iterací a roughness terénu
- Metoda `generate()` implementuje Diamond-Square algoritmus
- Výstupem je 2D matice výškových hodnot

### Třída FractalLandscapeApp
- Vytváří uživatelské rozhraní pomocí Tkinter
- Umožňuje nastavit parametry generování (počet iterací, roughness)
- Vizualizuje vygenerovanou krajinu ve 3D pomocí matplotlib

## Návrhy na vylepšení algoritmu

1. **Adaptivní persistence** - Místo konstantního násobitele 0.5 pro zmenšování náhodnosti by bylo možné implementovat parametr persistence H, který by umožnil generovat různé typy krajin (od hladkých po velmi členité):
   ```python
   roughness *= 2 ** (-H)
   ```

2. **Optimalizace výpočtu** - Současná implementace počítá některé průměry opakovaně. Bylo by možné použít memoizaci nebo přepracovat algoritmus pro efektivnější výpočty, což by bylo výhodné zejména při větších hodnotách iterací.

3. **Vícevrstevný terén** - Implementace generování více vrstev s různými parametry a jejich následné kombinování by umožnilo vytvářet realističtější krajiny s různými geologickými rysy (např. hory, údolí, plošiny).

4. **Omezení extremních hodnot** - Implementace omezení krajních hodnot, aby se zabránilo příliš vysokým vrcholům nebo příliš hlubokým údolím, které mohou vznikat v rozích mapy.

5. **Texturování** - Rozšíření o přiřazování textur na základě výšky a sklonu terénu by zvýšilo realističnost vizualizace.
