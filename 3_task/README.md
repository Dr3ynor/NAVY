# Popis Hopfieldovy sítě

## Vstupy a výstupy

### Vstupy

- Obrazce reprezentované binární maticí (0 = bílá, 1 = černá)
- Počet iterací pro rekonstrukci
- Režim rekonstrukce (synchronní/asynchronní)
- Prahová hodnota pro aktivaci neuronů
- Možnost přidání šumu do vstupního obrazce pro testování robustnosti

### Výstupy

- Rekonstruovaný obrazec
- Matice vah
- Seznam uložených vzorů
- Počet iterací do konvergence

## Jak funguje Hopfieldova síť

### 1. **Trénování**

Trénování sítě spočívá v ukládání vzorů do paměti sítě. Síť si pamatuje vzory prostřednictvím změny vah mezi neurony.

- Každý vstupní vzor je převeden do bipolární reprezentace (-1, 1), aby byla zajištěna symetrie při výpočtech.
- Matice vah se aktualizuje pomocí Hebbova pravidla (součinem vzoru se sebou samým), což umožňuje sítě naučit se vzor.
- Diagonální prvky matice vah jsou nulové, což zajišťuje, že neurony nemají vlastní zpětné vazby.
- Váhy mohou být normalizovány pro lepší stabilitu a snížení rizika přetížení sítě.
- Pokud se ukládá více vzorů, může dojít k efektu interferencí mezi nimi, což omezuje kapacitu sítě.

### 2. **Rekonstrukce**

Po naučení vzorů lze síť použít k rekonstrukci neúplných nebo šumem narušených vstupů.

- **Synchronní režim**: Všechny neurony se aktualizují najednou podle váhové matice.
- **Asynchronní režim**: Neurony se aktualizují postupně v náhodném pořadí.
- Stav neuronů se vypočítává na základě součtu vážených vstupů a porovnává se s prahovou hodnotou.
- Pokud se stav sítě stabilizuje (nedochází ke změnám mezi iteracemi), rekonstrukce končí.
- Síť může skončit v globálním minimu odpovídajícím naučenému vzoru, ale také může uvíznout v lokálním minimu.

## Možná vylepšení

- Implementace pravidla pro omezení paměti (omezit počet uložených vzorů)
- Optimalizace asynchronní aktualizace pro lepší konvergenci a snížení výpočetní náročnosti
- Experimentování s různými aktivačními funkcemi, například signum nebo sigmoidální aktivace
