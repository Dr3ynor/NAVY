# XOR problém
## Popis
Tento skript implementuje trénování jednoduché neuronové sítě pro řešení XOR problému.

Vstupní vrstva: Dvě vstupní neurony odpovídající hodnotám X1​ a X2​.
Skrytá vrstva: Dva neurony s sigmoidní aktivační funkcí.
Výstupní vrstva: Jeden neuron, jehož výstup je hodnotou buď 0 nebo 1, což reprezentuje predikci pro XOR.

Tento skript zahrnuje implementaci forward passu, zpětné propagace, aktualizace vah a biasů a výpočtu chyby pomocí metriky SSE.

Detailnější popis jednotlivých proměnných a funkcí lze najít přímo v souboru 2_task/main.py.
## Případné vylepšení
Neuronová síť má "napevno" daný počet vrstev/neuronů na XOR problém nebo na jiný problém, který vyžaduje maximálně 2 neurony a jeden výstupní neuron.

### Implementace dalších aktivačních funkcí
Bylo by zavhodno v rámci zobecnění neuronové sítě naimplementovat další aktivační funkce mimo sigmoid funkci, která se hodí na problémy, které mají dva možné výsledky.

### Přidat CLI

### Upravit learning rate a počet epoch
