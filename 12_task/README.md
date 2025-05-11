# Simulace celulárního automatu

Tento program představuje interaktivní simulaci šíření lesního požáru pomocí celulárního automatu.

## Jak program funguje

Program simuluje les jako mřížku buněk, kde každá buňka může být v jednom ze čtyř stavů:
- **Prázdná** (černá) - místo bez stromů
- **Strom** (zelená) - zdravý strom
- **Hořící** (červená) - strom, který právě hoří
- **Spálený** (šedá) - spálený strom

Simulace se řídí několika pravidly:
1. V prázdné buňce může s určitou pravděpodobností vyrůst strom
2. Strom začne hořet, pokud sousedí s hořícím stromem
3. Strom může také spontánně začít hořet s malou pravděpodobností
4. Hořící strom se po určité době změní na spálený
5. Spálený strom se může časem změnit zpět na prázdnou buňku

## Ovládací prvky

Simulace obsahuje několik posuvníků, které umožňují měnit parametry:
- **Growth Probability (p)** - pravděpodobnost, že na prázdném místě vyroste strom
- **Ignition Probability (f)** - pravděpodobnost spontánního vznícení stromu
- **Initial Forest Density** - počáteční hustota lesa při resetu simulace
- **Burnout Probability** - pravděpodobnost, že hořící strom shoří (změní se na spálený)
- **Regrow Probability** - pravděpodobnost, že spálený strom se změní na prázdné místo

Dále lze nastavit:
- **Typ sousedství**:
  - **von_neumann** - pouze 4 sousedi (nahoře, vpravo, dole, vlevo)
  - **moore** - všech 8 sousedů (včetně diagonálních)
- Tlačítko **Reset** - obnoví simulaci s aktuálním nastavením
