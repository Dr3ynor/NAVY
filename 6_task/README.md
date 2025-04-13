# 3D Fraktální generátor

## Popis kódu

Tento skript generuje a vizualizuje dvě různé 3D fraktální struktury využívající systém iterated function system (IFS). Program používá náhodný proces pro vytváření bodů v prostoru.

### Hlavní funkce

1. **`apply_transform(point, transform)`**: 
   - Aplikuje afinní transformaci na bod v 3D prostoru
   - Vstupem je bod jako trojice souřadnic (x, y, z) a transformační matice (12 parametrů)
   - Vrací nové souřadnice bodu po aplikaci transformace

2. **`generate_fractal(transforms, probabilities, iterations, start_point)`**:
   - Iterativně vybírá transformace s danou pravděpodobností a aplikuje je na aktuální bod
   - Začíná s výchozím bodem (defaultně na souřadnicích [0, 0, 0])
   - Provede specifický počet iterací (defaultně 50 000)
   - Vrací tři seznamy souřadnic x, y a z všech vygenerovaných bodů

### Modely fraktálů

Kód definuje dva modely fraktálů pomocí různých sad transformací:

1. **První model (`first_model_transforms`)**:
   - Připomíná 3D kapradinu
   - Používá čtyři transformace s rovnoměrným rozdělením pravděpodobností
   - Vytváří strukturu, která má hlavní "stonek" a "listy" vyrůstající do různých směrů

2. **Druhý model (`second_model_transforms`)**:
   - Vykazuje více větvení a jinou strukturu než první model
   - Používá také čtyři transformace s rovnoměrným rozdělením pravděpodobností
   - Vytváří více vertikálně orientovaný objekt s komplexním rozvětvením

### Vizualizace

Pro vizualizaci kódu se používá knihovna Plotly, která umožňuje interaktivní zobrazení 3D struktur:

- Pro každý model je vytvořen samostatný 3D bodový graf
- Je možné s nimi interaktivně manipulovat (rotace, přiblížení)

## Možná vylepšení

**Optimalizace výkonu**:
- Implementace vektorových operací s NumPy místo individuálního zpracování bodů
- Využití paralelního zpracování pro generování více modelů současně
