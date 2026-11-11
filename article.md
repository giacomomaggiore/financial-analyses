## <b>Opinioni forti</b>

Qualche giorno fa, <a href="https://www.toobigtofail.it/la-verita-dietro-il-kid-dei-prodotti-finanziari-ep-118/" target="_blank">mentre ascoltavo uno dei miei podcast preferiti</a>, rimasi quasi stupito dall'affermazione _(volutamente provocatoria)_ di uno degli host: "<b>90/60 + <a href="https://www.imgp.com/us/dbmf/" target="_blank">DBMF</a> è ormai Pareto superior a 60/40"</b>, con il non-troppo-implicito sottotesto: "se hai ancora un 60/40 sei un coglione".

Pur essendo generalmente d'accordo _(e avendo in portafoglio un'allocazione simile),_ mi è venuta la naturale curiosità di guardare i numeri alla base di questo claim.

Per i fan di _"<a href="https://www.vanguard.co.uk/professional/product/etf/equity/9679/ftse-all-world-ucits-etf-usd-accumulating" target="_blank">VWCE</a> & chill",_ breve recap:
- per 60/40 si intende generalmente un portafoglio composto al 60% da azioni (solitamente di aziende diversificate a livello globale) e al 40% da obbligazioni (qui la scelta è più complessa e dipende dal paese o dalla valuta di riferimento);
- per 90/60 si intende invece un'esposizione al 90% in azioni e al 60% in obbligazioni, ottenuta tramite l'utilizzo di <b>contratti futures obbligazionari</b>. 
- _Lastly,_ DBMF è un ETF che cerca di replicare la performance dei maggiori fondi di <b>managed futures</b> (CTA funds) che operano tramite trend following

Di conseguenza, la ratio dietro un portafoglio 90/60 + managed futures _(da qui in avanti: "model portfolio")_ è quella di combinare la <b>capital efficiency</b>, ossia l'uso efficiente del capitale e quindi della leva finanziaria per sfondare il muro del 100% e liberare spazio per altre asset class; con i managed futures, in grado di  offrire diversificazione aggiuntiva anche quando bonds e stocks vanno in rosso.

Dal punto di vista pratico, per il 90/60 si possono considerare i due ETF più diffusi: 
- <a href="https://www.nasdaq.com/market-activity/etf/ntsx" target="_blank">NTSX</a> _(90% equities US + 60% futures su <a href="https://www.cmegroup.com/trading/interest-rates/basics-of-us-treasury-futures.html" target="_blank">Treasury USA</a>)_
- <a href="https://www.marketwatch.com/investing/fund/ntsg" target="_blank">NTSG</a> _(90% equities dei mercati sviluppati con un <s>spiacevole</s> filtro ESG + 60% futures su titoli di Stato di paesi sviluppati)_

mentre per i managed futures, a seconda di investire in prodotti UCITS o meno, esistono diversi ETF oltre a DBMF che offrono esposizione trend following tramite contratti futures.

Dettagli e approfondimenti disponibili nell'appendice tecnica in coda all'articolo e nel relativo [notebook Python](https://github.com/giacomomaggiore/financial-analyses/blob/main/03_pareto_superiority_90_60.ipynb) su Github.

---

## <b>Reverse Engineering</b>

L'idea dietro questa breve analisi è, _again_, capire se "regge" la Pareto superiority, o, _in altre parole,_ studiare la performance relativa del model portfolio rispetto a un classico 60/40.

_Sulla carta,_ tutto sembra facile: prendi gli ETF menzionati, esegui un backtest di qualche decina d'anni, calcoli Sharpe e CAGR e il gioco è fatto. Peccato che NTSG abbia due anni di storia, DBMF poco di più e la scelta di un unico ETF di bond sia tutt'altro che scontata e dipenda fortemente dalla valuta di riferimento e dal paese di residenza.

Per quanto riguarda il 60/40 tuttavia, la soluzione è abbastanza semplice: una <b>combinazione lineare</b> degli indici <a href="https://www.msci.com/indexes/index/990100" target="_blank">MSCI World</a> Net Total Return e <a href="https://www.lseg.com/en/ftse-russell/indices/world-government-bond-index" target="_blank">FTSE WGBI Developed Markets</a> _(con una stima ottimistica di TER dello 0.10% per ciascuno)_, permette di avere una proxy per un ETF 100% azionario e un portafoglio 60/40.<br/>_(Nell'analisi, tuttavia, queste proxy sono sostituite con i rendimenti degli ETF "veri" quando disponibili per maggiore fedeltà.)_

Per NTSG la faccenda è <b>leggermente più complicata.</b>

_In primis,_ l'ETF investe tramite contratti futures che, _per loro natura,_ non hanno una serie di prezzi continua nel tempo, in quanto soggetti a delivery e rolling. Esistono ricostruzioni di serie storiche "aggiustate" che riconciliano il divario tra un contratto e l'altro, ma fare backtest su di esse comporta una serie di semplificazioni e l'omissione dei costi di transazione e roll.
<br/>_Secondariamente,_ NTSG ha una metodologia tutt'altro che semplice: oltre ad applicare un filtro ESG sulle azioni, investe in futures su titoli di Stato di Stati Uniti, Germania, Giappone e Regno Unito e ribilancia le posizioni periodicamente a febbraio, maggio, agosto e novembre o quando l'esposizione si discosta da quella target per oltre 5 punti percentuali.

Di conseguenza, sono partito da un modello semplificato di <b>return stacking</b>:

$$
R_{90/60,t}^{\mathrm{gross}}=0{,}90R_{E,t}+0{,}60R_{B,t}-0{,}50R_{cash,t}.
$$

dove $R_E$ è il ritorno dell'indice azionario, $R_B$ di quello obbligazionario e $R_{cash,t}$ rappresenta il costo del finanziamento.

La versione effettivamente usata nel backtest aggiunge il TER mensile della proxy (0.25% annuo) e un drag $d = 0,50 \%$ annuo sul nozionale obbligazionario:

$$
R_{90/60,t}^{\mathrm{net}}\approx0{,}90R_{E,t}+0{,}60R_{B,t}-0{,}50R_{cash,t}-c_{TER,m}-0{,}60\frac{d}{12},
\qquad c_{TER,m}=1-(1-0{,}25\%)^{1/12}.
$$


_(Da dicembre 2024 il backtest usa invece i rendimenti reali osservati di NTSG e non più l'ETF replicato sinteticamente)_

Il limite principale di questo modello è che un indice di obbligazioni cash unhedged, _misurato in USD,_ incorpora il cambio sul valore dell’intera posizione. _Al contrario,_ un future su obbligazioni estere non implica necessariamente un’esposizione valutaria sull’intero nozionale: contano la valuta del contratto, dei margini e la conversione del P&L.

Per quanto riguarda DBMF, la metodologia disponibile non è sufficiente per ricostruire fedelmente le esposizioni storiche ai singoli contratti futures né per replicare il Dynamic Beta per ogni fondo CTA tracciato.<br/>
Di conseguenza, ho considerato tre possibili <b>indici proxy</b> (<a href="https://ionanalytics.com/barclayhedge/indices/" target="_blank">SG Trend</a>, <a href="https://ionanalytics.com/barclayhedge/indices/" target="_blank">SG CTA</a> e <a href="https://portal.barclayhedge.com/cgi-bin/indices/displayHfIndex.cgi?indexCat=Barclay-Investable-Benchmarks&amp;indexName=BTOP50-Index" target="_blank">BarclayHedge BTOP50</a>) e il fattore <a href="https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum" target="_blank">AQR TSMOM</a>, e li ho confrontati con DBMF nei mesi comuni _(giugno 2019/maggio 2026)_ osservandone la correlazione. 
SG CTA risulta il più affine _(maggiore correlazione, minore tracking error),_ ed è dunque scelto come proxy sintetica tra il 2000 e il 2019, mentre per gli anni precedenti sono stati considerati i ritorni di BTOP50 e per quelli successivi le performance di DBMF in carne e ossa.

Avendo dunque tutti gli ingredienti sul tavolo, restano alcuni parametri liberi da scegliere/calibrare (principalmente legati alle stime dei costi dei futures, delle fee dei prodotti e delle strategie di ribilanciamento). _Again,_ dettagli tecnici e la ratio dietro ogni scelta nell'appendice.

## <b>Gli anni di Cristo e qualcosina in più</b> 

Il backtest in USD copre dal 1990 al 2026 confrontando 60/40 e 100% stocks con il model portfolio. 
Nella sua versione in EURO senza hedging valutario, _a parità di configurazione iniziale,_ il fattore valutario è comune e di conseguenza le performance relative sono necessariamente preservate. _Al contrario,_ volatilità, drawdown e rapporti di rischio-rendimento restano <b>sensibili al cambio valuta.</b>

![Crescita di 100.000 USD: confronto tra model portfolio, 60/40 e 100% azioni](images/pareto-performance-1990-2026.png)

![Ricchezza relativa al 60/40: model portfolio e 100% azioni, rapporto iniziale pari a 1](images/pareto-relative-wealth-1990-2026.png)


| Portafoglio  | CAGR | Volatilità | Max drawdown | Average drawdown | Ulcer index | Sharpe | Sortino | Calmar |
| ---  | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 90/60 + managed futures  | 7.51% | 10.35% | -32.25% | -4.37% | 7.23% | 0.49 | 0.75 | 0.23 |
| 60/40 |  6.63% | 9.94% | -34.24% | -4.43% | 7.90% | 0.43 | 0.62 | 0.19 |
| 100% stocks  | 7.96% | 15.02% | -54.09% | -9.48% | 15.31% | 0.41 | 0.58 | 0.15 |


_L’average drawdown è la media dei drawdown di fine mese sull’intero periodo, inclusi i mesi con drawdown nullo ed esclusa la data iniziale._

_Tirando un po' le somme...._ se volessimo fare i "pignolazzi", in questa configurazione il model portfolio <b>NON risulta Pareto superior</b> a un classico 60/40 _(si noti infatti la maggiore volatilità)_ ma, assumendo un buon margine d'errore e chiudendo un occhio, <b>la tesi regge</b>.

A fronte di 41 basis point di volatilità in più, il model portfolio presenta un <b>CAGR maggiore</b> (7.51% vs 6.63%) e un drawdown medio leggermente meno profondo rispetto a un classico 60/40.
Si noti anche che, _senza troppe sorprese vista la presenza di un ulteriore diversificatore (i managed futures!),_ il model portfolio offre anche un profilo di rischio più conservativo rispetto al 100% stocks.
In questo caso infatti, a fronte di un CAGR tutto sommato simile (7.51% vs 7.96%), il model portfolio presenta volatilità e average drawdown nettamente inferiori in valore assoluto (10.35% vs 15.02% e -4.37% vs -9.48%).

Facendo uno step avanti nell'analisi, emergono _(almeno)_ altre due cose worth mentioning:
- la deviazione standard dei rendimenti cumulati rolling su 12 mesi _(e di conseguenza il rischio di sequenza)_ è simile tra model portfolio e 60/40 (10.35% vs 9.97%), mentre è più alta per il 100% stocks (15.87%).

![Rendimenti cumulati rolling a 12 mesi: model portfolio, 60/40 e 100% azioni](images/pareto-rolling-12-month-returns.png)

- la correlazione rolling a sei mesi tra managed futures e 100% equities <b>diminuisce durante i bear market azionari</b>, a dimostrazione del fatto che il diversificatore funziona soprattutto nei momenti in cui tutto sembra andare a puttane. _Al contrario,_ nei momenti di forti bull market (esattamente come dal covid a oggi), difficile overperformare le azioni in termini di rendimento atteso.

![Correlazione rolling a 6 mesi tra model portfolio e azioni, con regime azionario USD](images/pareto-rolling-correlation-equities.png)

![Managed futures e azioni: rendimento totale e correlazione rolling](images/managed-futures-equities-correlation.png)

Lungi da me 1) promuovere NTSG 2) denigrare VWCE & chill 3) sfidare<a href="https://theitalianleathersofa.com/blog/" target="_blank"> gente che ne sa molto più di me... </a>Numeri e commenti nascono solo da una curiosità e dalla necessità di modellare un problema nel modo più accurato possibile, anche quando dati e regole del gioco sono tutt'altro che chiari.

Secondariamente, come già accennato qui, attribuisco rilevanza molto limitata ai backtest... se <b>"past performance is not indicative of future results"</b> è una delle frasi più abusate a Wall Street ci sarà un motivo!

Cheers!

---

## Reference

<a href="https://github.com/giacomomaggiore/financial-analyses/blob/main/03_pareto_superiority_90_60.ipynb" target="_blank">Source code (Python Notebook by Giacomo)</a>
<br/>
<a href="https://www.nasdaq.com/market-activity/etf/ntsx" target="_blank">WisdomTree U.S. Efficient Core Fund (NTSX) - Nasdaq</a>
<br/>
<a href="https://www.marketwatch.com/investing/fund/ntsg" target="_blank">WisdomTree Global Efficient Core UCITS ETF (NTSG) - MarketWatch</a>
<br/>
<a href="https://www.imgp.com/us/dbmf/" target="_blank">iMGP DBi Managed Futures Strategy ETF (DBMF) - iM Global Partner</a>
<br/>
<a href="https://www.lseg.com/en/ftse-russell/indices/world-government-bond-index" target="_blank">FTSE World Government Bond Index - factsheet e metodologia (LSEG)</a>
<br/>
<a href="https://www.cmegroup.com/trading/interest-rates/basics-of-us-treasury-futures.html" target="_blank">The basics of U.S. Treasury futures (CME Group)</a>
<br/>
<a href="https://ionanalytics.com/barclayhedge/indices/" target="_blank">SG Prime Services Indices e BTOP50 - indici e dati (BarclayHedge / ION Analytics)</a>
<br/>
<a href="https://www.toobigtofail.it/" target="_blank">TooBigToFail - Un podcast di finanza personale cialtrone</a>
<br/>



---

## Appendice

## A1. Metodologia

Il backtest usa rendimenti mensili in USD da gennaio 1990 ad agosto 2026. Il 60/40 e il 100% azionario sono costruiti con le rispettive serie storiche disponibili; il model portfolio combina un'esposizione azionaria del 90%, un'esposizione obbligazionaria target del 60% e una quota di managed futures. Quando disponibili, i rendimenti osservati di NTSG e DBMF sostituiscono le rispettive proxy sintetiche.

Per estendere il campione, il 90/60 è approssimato con indici azionari e obbligazionari più un drag annuo dello 0,50% applicato al nozionale obbligazionario; DBMF è invece rappresentato da SG CTA nel periodo 2000–2019 e da BTOP50 negli anni precedenti. I risultati rimangono quindi molto indicativi e sensibili alle scelte di indici e parametri di calibrazione.

| TICKER | Nome prodotto | Metodologia e info di base |
| --- | --- | --- |
| N/D (indice) | <a href="https://www.msci.com/indexes/index/990100" target="_blank">MSCI World Net Total Return</a> | Indice azionario dei mercati sviluppati, con dividendi netti reinvestiti; proxy azionaria storica in USD. Sostituito dai rendimenti osservati di URTH quando disponibili. |
| WGBI DM (indice) | <a href="https://www.lseg.com/en/ftse-russell/indices/world-government-bond-index" target="_blank">FTSE World Government Bond Index Developed Markets</a> | Obbligazioni governative investment-grade a tasso fisso e in valuta locale dei mercati sviluppati; serie USD non coperta dal cambio, usata come proxy obbligazionaria. Sostituita dai rendimenti osservati di IGLO quando disponibili. |
| USD T-bills (serie) | <a href="https://www.treasurydirect.gov/marketable-securities/treasury-bills/" target="_blank">U.S. Treasury Bills</a> | Rendimento mensile di riferimento per la liquidità/finanziamento in USD e per il tasso privo di rischio. |
| BTOP50 | <a href="https://portal.barclayhedge.com/cgi-bin/indices/displayHfIndex.cgi?indexCat=Barclay-Investable-Benchmarks&amp;indexName=BTOP50-Index" target="_blank">BarclayHedge BTOP50 Index</a> | Benchmark diversificato dei managed futures, basato sui rendimenti netti dei CTA; proxy principale del periodo 1990–1999. |
| SG CTA | <a href="https://ionanalytics.com/barclayhedge/indices/" target="_blank">SG CTA Index</a> | Indice di CTA con rendimenti netti dei gestori; proxy principale del periodo 2000–maggio 2019, scelta per maggiore affinità con DBMF nel confronto comune. |
| SG Trend | <a href="https://ionanalytics.com/barclayhedge/indices/" target="_blank">SG Trend Index</a> | Indice di strategie trend-following; usato come proxy candidata nel confronto con DBMF, non nella serie storica baseline. |
| TSMOM (fattore) | <a href="https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum" target="_blank">AQR Time Series Momentum</a> | Fattore momentum temporale su futures; serie di rendimenti in eccesso, confrontata con DBMF e utilizzabile per estensioni opzionali del campione prima del 1987. |
| URTH (ETF) | iShares MSCI World ETF | Rendimenti osservati dell’ETF azionario usati al posto della proxy MSCI World dopo l’inizio della serie disponibile. |
| IGLO (ETF) | iShares Global Government Bond UCITS ETF | Rendimenti osservati dell’ETF obbligazionario usati al posto della proxy FTSE WGBI dopo l’inizio della serie disponibile. |
| NTSG (ETF) | WisdomTree Global Efficient Core UCITS ETF | Rendimenti osservati usati al posto della proxy sintetica 90/60 da dicembre 2024. |
| DBMF (ETF) | iMGP DBi Managed Futures Strategy ETF | Rendimenti totali osservati, netti delle spese del fondo. |



## A2. Rischio valutario della proxy obbligazionaria

La proxy del 90/60 usa un indice di obbligazioni estere non coperto dal rischio di cambio. Nello specifico, il rendimento dell'indice totale si compone da prezzi, cedole del sottostante obbligazionario e del cambio valuta.

Un future obbligazionario si  espone al rendimento del titolo tramite margini e collaterale, senza richiedere l'acquisto dell'intero nozionale nella valuta estera. Di conseguenza, il 60% di un indice obbligazionario cash non equivale necessariamente al 60% di futures obbligazionari.

NTSG mantiene collaterale in USD, EUR, GBP e JPY; la proxy combina invece obbligazioni non coperte con finanziamento legato ai <a href="https://www.treasurydirect.gov/marketable-securities/treasury-bills/" target="_blank">T-bill USA</a>. Cambiano quindi esposizione valutaria, carry, finanziamento e collaterale. Il drag inserito nel modello rappresenta solo un costo ipotetico e non elimina queste differenze. Di conseguenza, volatilità, correlazioni e rendimenti della proxy rischiano di discostarsi da quelli di NTSG.

## A3. Sensibilità delle ipotesi

Sulla configurazione gennaio 1990–agosto 2026, il CAGR resta sensibile alle assunzioni di drag.

| Ipotesi | CAGR model portfolio |
| --- | ---: |
| Drag obbligazionario 0% annuo sul nozionale | 7.71% |
| Drag obbligazionario 0.50% annuo sul nozionale — baseline | 7.51% |
| Drag obbligazionario 1.00% annuo sul nozionale | 7.31% |
| Gross-up CTA ipotetico 2%/20%, con drag baseline | 8.52% |

Gli indici CTA usati come proxy riportano rendimenti netti delle commissioni dei gestori. Per stimare in via esplorativa un rendimento lordo, il notebook applica un modello ipotetico di fee 2/20 _(management fee del 2% annuo e performance fee del 20% sui nuovi massimi del NAV)._ La commissione di performance viene quindi invertita solo quando il NAV netto supera il precedente massimo storico.

_Tuttavia,_ la configurazione baseline non applica il gross-up. La configurazione 2/20 è mostrata soltanto come sensibilità: applicarla aumenterebbe il CAGR del model portfolio dal 7,51% all'8,52%. Il TER ipotetico della proxy managed futures resta comunque  applicato ai mesi sintetici.

## A4. Proxy NTSG

Utilizzando un drag pari a zero, il breve confronto tra NTSG e il proxy 90/60, da dicembre 2024 ad agosto 2026 mostra:

- correlazione mensile 0.990
- tracking error annualizzato 1.75%

_Ciò nonostante,_ il backtest  utilizza 0.50% annuo sul nozionale obbligazionario nei mesi sintetici per adottare un approccio più conservativo.