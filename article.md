
Qualche giorno fa, mentre ascoltavo uno dei miei podcast preferiti, rimasi quasi stupito dall'affermazione (provocatoria) di uno degli host: "90/60 + DBMF è ormai Pareto superior a 60/40", con il non troppo implicito sottotesto: "se hai ancora un 60/40 sei un coglione".

Pur essendo generalmente d'accordo (e avendo in portafoglio un'allocazione simile), mi è venuta la naturale curiosità di testare questa dichiarazione.

Per i fan di "VWCE & chill", breve recap:
- per 60/40 si intende generalmente un portafoglio composto al 60% da azioni (solitamente di aziende diversificate a livello globale) e al 40% da obbligazioni (qui la scelta è più complessa e dipende dal paese o dalla valuta di riferimento);
- per 90/60 si intende invece un portafoglio con un'esposizione del 90% alle azioni e del 60% alle obbligazioni, ottenuta tramite l'utilizzo di contratti futures obbligazionari. 
- _Lastly,_ DBMF è un ETF che cerca di replicare la performance dei maggiori fondi di managed futures che operano tramite trend following

Di conseguenza, la ratio dietro un portafoglio 90/60 + managed futures (da cui in avanti: il "model portfolio") è quello di combinare la capital efficiency, cioè l'uso efficiente del capitale e quindi della leva finanziaria per sfondare il muro del 100% e liberare spazio per altri diversificatori, in questo caso i managed futures, in grado di  offrire diversificazione anche quando bonds e stocks vanno in rosso.

Per il 90/60, si possono considerare i due ETF più diffusi: NTSX (90% equities US + 60% futures su Treasury USA) e NTSG (90% equities dei mercati sviluppati con un filtro ESG + 60% futures su titoli di Stato di paesi sviluppati), mentre per i managed futures, a seconda di investire in prodotti UCITS o meno, esistono diversi prodotti oltre a DBMF che offrono esposizione trend following tramite i futures.

Dettagli e approfondimenti disponibili nell'appendice tecnica in coda all'articolo e nel relativo [notebook Python](03_pareto_superiority_90_60.ipynb) su Github.

---

L'idea dietro questa breve analisi è, _again_, capire se "regge" la Pareto superiority, o, in altre parole, studiare la performance relativa del model portfolio rispetto a un classico 60/40.

Sulla carta, tutto sembra facile: prendi gli ETF menzionati, esegui un backtest di qualche decina d'anni, calcoli Sharpe e CAGR  e il gioco è fatto. Peccato che NTSG abbia due anni di storia, DBMF poco di più e la scelta per unico ETF di bond è tutt'altro che scontata e dipende fortemente  valuta di riferiento e paese di resdienza.

Per quanto riguarda il 60/40 tuttavia, la soluzione è abbastanza semplice: una combinazione lineare degli indici MSCI World net total return e FTSE WGBI Developed Markets total return (con una stima ottimistica di TER dello 0.10% per ciascuno), permette di avere una proxy per un ETF 100% azionario e un portafoglio 60/40. _(Nell'analisi, tuttavia, queste proxy sono sostituite i ritorni degli ETF "veri" per maggiore fedeltà.)_

Per NTSG la faccenda è leggermente più complicata. In primis, l'ETF investe tramite contratti futures che, per loro natura, non hanno una serie di prezzi continua nel tempo, in quanto soggetti a delivery e rolling, cioè alla sostituzione dei contratti in scadenza. Esistono delle serie storiche "aggiustate" che riconciliano il divario tra un contratto e l'altro, ma fare backtest su di esse comporta una serie di semplificazioni e l'omissione dei costi di transazione e roll.
Secondariamente, NTSG ha una metodologia tutt'altro che semplice: oltre ad applicare un filtro ESG alla sua selezione di azioni, investe in futures su titoli di Stato di Stati Uniti, Germania, Giappone e Regno Unito e ribilancia le posizioni periodicamente a febbraio, maggio, agosto e novembre o quando l'esposizione si discosta da quella target per olte 5 punti percentuali.

Di conseguenza, sono partito da un modello semplice di return stacking:

[]

in cui .... , per poi compicarlo leggermente aggiungtendo TER e un drag annuo pipotetico sul nozionale obligazionario per modellare gli attriti nel trading dei futures.

_(Come prima, da dicembre 2024 l'analisi usa invece i rendimenti reali osservati di NTSG e non più l'ETF replicato sinteticamente)_

Quello che ne risulta, più che una replica storica di NTSG, è un generico 90/60: la proxy non modella direttamente i contratti futures, il collaterale multivaluta, la selezione ESG o i margini giornalieri. In particolare, un indice di obbligazioni estere cash unhedged incorpora il cambio sull'intero capitale investito, mentre un future non implica automaticamente la stessa esposizione valutaria sul nozionale: contano conversione di profitti e perdite, margini e collaterale. 

Per quanto riguarda DBMF, le informazioni disponibili non sono sufficienti per ricostruire fedelmente il suo processo storico e le esposizioni ai singoli contratti futures. Inoltre, Il modello preciso di replicazione è ovviamente proprietario e, pur essendo descritto nei suoi principi generali; npn è sufficiente trasparente a ricavarne una replica accurata.

Di conseguenza, ho considerato tre possibili indici proxy di DBMF (SG Trend, SG CTA e BarclayHedge BTOP50), oltre al fattore AQR TSMOM, e li ho confrontati con DBMF nei mesi comuni da giugno 2019 a maggio 2026 paragonandone la correlazione. 
Il più affine (maggiore correlazione, minore tracking error) è risultato SG CTA, scelto dungque come proxy sintetica tra il 2000 e il 2019, mentre per gli anni precedenti  sono stati considderati i ritorni di BT0P50 e per queli successivi le performnace di DBMF iun carne e ossa. come ipotesi.

Avendo dunque tutti gli ingredienti sul tavolo, restano alcuni parametri liberi da scegliere/calibrare (principalmente legati alle stime dei costi dei futures, delle fee dei prodotti e delle strategie di ribilanciamento). _Again,_ dettagli tecnici e la ratio dietro ogni scelta nell'appendice.

Il backtest in USD copre rendimenti mensili dal 1990 al 2026 e confronta il 60/40 e il 100% stocks con un model portfolio. 
Nella sua versione in EURO senza hedging valtario,, a parità di condigurazione iniziale, il fattore valutario è comune e di conseguenza le performance relative sono necessariamente preservato. Al contrario, volatilità, drawodn e rapporti dirschi rendimento restano sensibili al camio valuta.

![Crescita di 100.000 USD: confronto tra model portfolio, 60/40 e 100% azioni](images/pareto-performance-1990-2026.png)

![Ricchezza relativa al 60/40: model portfolio e 100% azioni, rapporto iniziale pari a 1](images/pareto-relative-wealth-1990-2026.png)


| Portafoglio | Rendimento totale | CAGR | Volatilità | Max drawdown | Average drawdown | Ulcer index | Sharpe | Sortino | Calmar |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 90/60 + managed futures | 1321.61% | 7.51% | 10.35% | -32.25% | -4.91% | 7.23% | 0.49 | 0.75 | 0.23 |
| 60/40 | 950.88% | 6.63% | 9.94% | -34.24% | -4.62% | 7.90% | 0.43 | 0.62 | 0.19 |
| 100% stocks | 1560.24% | 7.96% | 15.02% | -54.09% | -6.78% | 15.31% | 0.41 | 0.58 | 0.15 |


Tirando un po' le somme.... se volessimo fare i "pignolazzi", almeno secondo questa simulazione, il model portfolio NON risulta Pareto SUperior a un classico 60/40 (si noti infatti la maggiore volatilità e l'average drawdown) ma, assumendo un buon margine d'errore e chiudendo un occhio, la tesi del podcast regge.

A fronte di 41 basis point di volatilità annualizzata in più e un drawodn medio leggermente più profondo, il model portfolio presenta nel campione un CAGR maggiore (7.51% vs 6.63%)rispetto a un classico 60/40.
Si noti che, senza troppe sorprese vista la presenza di un ulteriore diversificatore (i managed futures!), il model portfolio offre anche un profilo di rischio più conservativo rispetto al 100% stocks.
In questo caso infatti, a fronte di un CAGR tuttosommato simile (7.51% vs 7.96%), il model portfolio presenta volatilità e average drawdown nettamenti inferiori in valore assoluto (10.35% vs 15.02% e -4.91% vs -6.78%).

Facendo uno step avanti nell'analisi, emergono (almeno) altre due cose worth mentioning:
- la deviazione standard dei rendimenti cumulati rolling su 12 mesi è simile tra model portfolio e 60/40 (10.35% vs 9.97%), mentre è più alta per il 100% stocks (15.87%).
- la correlazione rolling a sei mesi tra managed futures e 100% equities diminuisce durante i bear market azionari, a dimostrazione del fatto che il diversificatore funziona soprattutto nei momenti ni cui tutto sembra andare a puttane. Al contrario, nei momenti di fortin bull marketq  (esattamente come dal covid a oggi), difficile battere le azioni in termini di rendimento atteso

Come controllo esplorativo ho effettuato un **bootstrap circolare a blocchi appaiati**, mantenendo insieme i rendimenti mensili del model portfolio e del 60/40. Ogni ricampionamento conserva la lunghezza del campione originale; i blocchi possono proseguire dalla fine all'inizio della serie. Il notebook rende riproducibile il calcolo con seed 20261110 e blocchi di 6, 12, 24 e 60 mesi, analizzati in quest'ordine con un unico generatore casuale.

Lunge da me 1) promuovere NTSG 2) denigrare VWCE & chill 3) smentire gente che ne sa molto più di me... Numeri e commenti proposti sono nascono solo da una curiosità e dalla necessità di scomporre e modellare un problea nel modo piùà accurato possibile, anche quando dati e regole del gioco sono tutt'altro che chiare.
Secondariamente, come già accennato qui, attribuisco rilevanza molto limitata ai backtest... se "past performance is not indicative of future results" è una delle frasi più abusate a Wall Steet ci sarò un motivo!

---

## Appendice A — Rischio valutario della proxy obbligazionaria

Un indice di obbligazioni estere cash non coperto incorpora il cambio sull'intero capitale investito. Se $X_t$ è il valore in USD di un'unità della valuta estera, il rendimento di un'obbligazione detenuta direttamente è:

$$
1+R_{B,USD,t}=(1+R_{B,locale,t})\frac{X_t}{X_{t-1}}.
$$

Il cambio rivaluta quindi anche il capitale iniziale, non soltanto gli interessi o la variazione del prezzo locale. Nella proxy, applicare un peso del 60% a un indice cash unhedged porta con sé questa esposizione valutaria.

Un future obbligazionario, invece, non richiede di investire l'intero nozionale nella valuta del sottostante. Genera profitti e perdite, regolati tramite margini, e richiede collaterale. Per un contratto regolato in valuta estera, rilevano la conversione dei flussi di margine e l'esposizione della liquidità detenuta in quella valuta: il solo nozionale non equivale automaticamente a una posizione valutaria cash dello stesso importo.

NTSG detiene collaterale in USD, EUR, GBP e JPY, mentre la proxy combina obbligazioni cash non coperte e finanziamento riferito ai T-bill USD. Differiscono quindi esposizione valutaria, carry, finanziamento e dinamica del collaterale, oltre a duration e pesi per paese. Un drag costante può rappresentare un costo ipotetico, ma **non corregge queste differenze strutturali**, che possono modificare anche volatilità e correlazioni. La metodologia ufficiale è richiamata nella [descrizione di NTSG](methodology/NTSG.md).

## Appendice B — Sensibilità delle ipotesi

Sulla configurazione gennaio 1990–agosto 2026, modificando un'ipotesi alla volta e lasciando invariati i mesi con rendimenti effettivi degli ETF:

| Ipotesi | CAGR model portfolio |
| --- | ---: |
| Drag obbligazionario 0% annuo sul nozionale | 7.71% |
| Drag obbligazionario 0.50% annuo sul nozionale — baseline | 7.51% |
| Drag obbligazionario 1.00% annuo sul nozionale | 7.31% |
| Gross-up CTA ipotetico 2%/20%, con drag baseline | 8.52% |

Il gross-up sposta il CAGR di circa **1.01 punti percentuali annui**, mentre dimezzare o raddoppiare i costi di trading dell'investitore lo porta rispettivamente a circa **7.52% e 7.48%**. Il gross-up è un'inversione ipotetica delle commissioni degli indici CTA aggregati, non una ricostruzione verificata delle commissioni dei singoli gestori. Questi scenari misurano la sensibilità alle assunzioni, non costituiscono intervalli di confidenza né giustificano la scelta del caso più favorevole.

## Appendice C — Qualità della proxy NTSG

Sul breve confronto con il NAV ufficiale, da dicembre 2024 ad agosto 2026, il notebook produce:

- correlazione mensile **0.990**;
- tracking error annualizzato **1.75%**;
- **21 osservazioni mensili**.

Questa diagnostica usa la proxy non calibrata con **drag zero**, mentre il backtest principale utilizza lo 0.50% annuo sul nozionale obbligazionario nei mesi sintetici. Il NAV include già le spese del fondo. La correlazione elevata è incoraggiante, ma risente della grande componente azionaria comune: un campione così breve non verifica la fedeltà della proxy nei diversi regimi storici né elimina la differenza valutaria descritta nell'Appendice A.

