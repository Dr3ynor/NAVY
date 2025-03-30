# Q-learning v úloze hledání sýra

Tento dokument vysvětluje implementaci algoritmu Q-learning na příkladu agenta hledajícího sýr v dvojrozměrném prostředí.

## Obsah
1. [Základní princip Q-learningu](#základní-princip-q-learningu)
2. [Matematický základ](#matematický-základ)
3. [Analýza kódu](#analýza-kódu)
4. [Vstupy a výstupy](#vstupy-a-výstupy)
5. [Vizualizace a interakce](#vizualizace-a-interakce)

## Základní princip Q-learningu

Q-learning je algoritmus tzv. reinforcement learning, který umožňuje agentům naučit se optimální chování v prostředí na základě systému odměn a trestů. Agent se postupně učí, které akce jsou v daných stavech nejvýhodnější, aniž by potřeboval předem znát model prostředí.

V kontextu naší úlohy:
- **Agent** je entita, která se pohybuje po mřížce
- **Prostředí** je 2D mřížka obsahující sýr (cíl) a díry (nebezpečí)
- **Stavy** jsou pozice agenta v mřížce
- **Akce** jsou pohyby ve čtyřech směrech (nahoru, dolů, vlevo, vpravo)
- **Odměny** jsou kladné za nalezení sýra, záporné za spadnutí do díry a mírně záporné za každý krok (motivace k rychlému dosažení cíle)

## Matematický základ

Q-learning vytváří tzv. Q-tabulku, která pro každou kombinaci stavu a akce udržuje hodnotu Q(s,a) - očekávanou kumulativní odměnu při vykonání akce 'a' ve stavu 's' a následování optimální strategie.

### Bellmanova rovnice

Hodnoty Q(s,a) jsou aktualizovány podle Bellmanovy rovnice:

```
Q(s,a) = Q(s,a) + α * [r + γ * max(Q(s',a')) - Q(s,a)]
```

kde:
- **s** je aktuální stav
- **a** je vykonaná akce
- **r** je získaná okamžitá odměna
- **s'** je nový stav po provedení akce
- **α** (alpha) je míra učení (0 < α ≤ 1)
- **γ** (gamma) je discount faktor určující důležitost budoucích odměn (0 ≤ γ < 1)

### Strategie výběru akcí (ε-greedy)

Pro rovnováhu mezi prozkoumáváním nových akcí a využíváním již známých optimálních akcí se používá ε-greedy strategie:
- S pravděpodobností ε agent vybere náhodnou akci (exploration)
- S pravděpodobností (1-ε) agent vybere akci s nejvyšší Q-hodnotou (exploitation)

## Analýza kódu

Pojďme se podívat na klíčové části implementace Q-learningu v poskytnutém kódu.

### Inicializace Q-tabulky

```python
Q = np.zeros((ROWS, COLS, 4))  # 4 akce: R, L, D, U
actions = [(0,1),(0,-1),(1,0),(-1,0)]  # R, L, D, U
```

Q-tabulka je reprezentována trojrozměrným polem, kde:
- První dvě dimenze (ROWS, COLS) reprezentují pozici agenta
- Třetí dimenze (4) reprezentuje možné akce (vpravo, vlevo, dolů, nahoru)

### Parametry algoritmu

```python
alpha = 0.1  # Rychlost učení
gamma = 0.9  # Discount faktor
epsilon = 0.1  # Explorační faktor
```

- **alpha = 0.1**: Míra učení určující, jak rychle se agent přizpůsobuje novým informacím
- **gamma = 0.9**: Discount faktor určující důležitost budoucích odměn
- **epsilon = 0.1**: Pravděpodobnost, že agent zvolí náhodnou akci (10%)

### Výběr akce

```python
def choose_action(y, x, greedy=False):
    if not greedy and random.random() < epsilon:
        return random.randint(0, 3)
    return np.argmax(Q[y, x])
```

Tato funkce implementuje ε-greedy strategii:
- Pokud je generováno náhodné číslo menší než epsilon, agent zvolí náhodnou akci
- Jinak agent zvolí akci s nejvyšší Q-hodnotou
- Parametr `greedy=True` umožňuje vždy vybrat nejlepší akci (používá se při demonstraci naučeného chování)

### Systém odměn

```python
def get_reward(y, x):
    if board[y, x] == 'C':
        return 10
    elif board[y, x] == 'O':
        return -10
    return -0.1
```

Systém odměn:
- +10 za nalezení sýra
- -10 za spadnutí do díry
- -0.1 za každý krok (motivace k nalezení nejkratší cesty)

### Aktualizace Q-hodnot

```python
r = get_reward(ny, nx)
Q[y, x, a] = Q[y, x, a] + alpha * (r + gamma * np.max(Q[ny, nx]) - Q[y, x, a])
```

Tato část implementuje Bellmanovu rovnici pro aktualizaci Q-hodnot:
1. Získá okamžitou odměnu `r` za nový stav
2. Vypočítá maximální Q-hodnotu pro nový stav `np.max(Q[ny, nx])`
3. Aktualizuje Q-hodnotu pro původní stav a zvolenou akci

### Tréninkový krok

```python
def train_step():
    global current_episode, current_step, walker_pos, agent_path, episode_successes, training_in_progress
    
    # Pokud začínáme novou epizodu
    if current_step == 0:
        walker_pos = [0, 0]
        agent_path = [(0, 0)]
    
    # Jeden krok Q-learningu
    y, x = walker_pos
    a = choose_action(y, x)
    dy, dx = actions[a]
    ny, nx = y + dy, x + dx
    
    # Hranice mapy
    if not (0 <= ny < ROWS and 0 <= nx < COLS):
        ny, nx = y, x
        
    # Aktualizace agenta
    walker_pos = [ny, nx]
    agent_path.append((nx, ny))
    
    # Výpočet odměny a aktualizace Q-tabulky
    r = get_reward(ny, nx)
    Q[y, x, a] = Q[y, x, a] + alpha * (r + gamma * np.max(Q[ny, nx]) - Q[y, x, a])
    
    # Kontrola ukončení epizody
    current_step += 1
    episode_ended = False
    
    if board[ny, nx] == 'C':  # Sýr nalezen - úspěch
        episode_ended = True
        episode_successes += 1
    elif board[ny, nx] == 'O':  # Díra - neúspěch
        episode_ended = True
    elif current_step >= 100:  # Limit kroků - neúspěch
        episode_ended = True
    
    # ... (další kód pro ukončení epizody)
```

Tato funkce implementuje jeden tréninkový krok algoritmu:
1. Vybere akci pomocí ε-greedy strategie
2. Provede akci a přesune agenta na novou pozici
3. Získá odměnu za nový stav
4. Aktualizuje Q-hodnotu pro původní stav a provedenou akci
5. Kontroluje, zda epizoda skončila (nalezení sýra, spadnutí do díry, překročení limitu kroků)

## Vstupy a výstupy

### Vstupy

1. **Konfigurace prostředí:**
   - Velikost mřížky (ROWS, COLS)
   - Pozice překážek (děr) a cíle (sýra)

2. **Parametry učení:**
   - Rychlost učení (alpha)
   - Discount faktor (gamma)
   - Explorační faktor (epsilon)

3. **Uživatelské vstupy přes GUI:**
   - Úpravy prostředí (přidávání/odebírání sýra a děr)
   - Spuštění tréninku
   - Spuštění demonstrace naučeného chování
   - Nastavení vizualizace

### Výstupy

1. **Q-tabulka:**
   - Matice Q-hodnot pro každou kombinaci stavu a akce
   - Reprezentuje naučenou strategii agenta

2. **Vizuální výstupy:**
   - Zobrazení prostředí a pohybu agenta
   - Vizualizace Q-hodnot
   - Vizualizace cesty agenta

3. **Statistické výstupy:**
   - Graf úspěšnosti tréninku
   - Počet úspěšných epizod
   - Průměrný počet kroků k cíli

## Vizualizace a interakce

Kód obsahuje komplexní vizualizaci pomocí knihovny Pygame:

1. **Zobrazení herní plochy:**
   - Mřížka s agentem, sýrem a dírami
   - Vizualizace cesty agenta
   - Zobrazení Q-hodnot pro každou buňku

2. **Interaktivní panely:**
   - Panel pro úpravu mapy (přidávání/odebírání objektů)
   - Panel pro ovládání učení (spuštění tréninku, resetování)
   - Panel pro nastavení vizualizace

3. **Historie učení:**
   - Graf úspěšnosti tréninku
   - Zobrazení statistik o úspěšnosti agenta

### Příklad interakce s aplikací:

1. Uživatel nastaví prostředí (pozice sýra a děr)
2. Spustí trénink agenta (50 epizod)
3. Sleduje proces učení a vývoj Q-hodnot
4. Spustí demonstraci naučeného chování agenta
5. Analyzuje výsledky pomocí grafů a statistik


4. **Případné vylepšení**

Kód by mohl benefitovat z rozdělení do objektově orientované struktury, která by oddělila logiku Q-learningu, vykreslování a řízení aplikace. Bylo by vhodné přidat více konfiguratelných parametrů (epsilon, alpha, gamma) přes GUI místo pevně daných hodnot. 


## Shrnutí

Q-learning je efektivní algoritmus pro učení optimálního chování v prostředí bez předchozí znalosti modelu. V této implementaci se agent učí hledat sýr v dvojrozměrném prostředí s překážkami. Algoritmus postupně vytváří Q-tabulku, která reprezentuje očekávané odměny pro každou kombinaci stavu a akce. 

Po dostatečném tréninku je agent schopen najít optimální cestu k sýru, vyhnout se dírám a maximalizovat celkovou odměnu. Vizualizace a interaktivní prvky umožňují sledovat proces učení a analyzovat výsledky.