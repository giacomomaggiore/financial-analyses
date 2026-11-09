
Qualche giorno fa, mentre ascoltavo uno dei miei podcast preferiti, rimasi quasi stupito dall'affermazione (provocatoria) di uno degli host: "il portafoglio 90/60 è Pareto superior al 60/40", con il non troppo implicito sottotesto: "se hai ancora un 60/40 sei un coglione".

Pur essendo generalmente d'accordo (e avendo da qualche mese in portafoglio un ETF che replica la prima allocazione, oltre a essere interessato a leva e return stacking, beh...), mi è venuta la naturale curiosità di testare questa dichiarazione.

Per chi non ne fosse al corrente:
- per 60/40 si intende generalmente un portafoglio composto al 60% da azioni (solitamente di aziende diversificate a livello globale) e al 40% da obbligazioni (qui la scelta è più complessa e dipende dal paese o dalla valuta di riferimento);
- per 90/60 si intende invece un portafoglio con un'esposizione del 90% alle azioni e del 60% alle obbligazioni, ottenuta tramite l'utilizzo di contratti future. Più nel dettaglio, il portafoglio è investito per il 90% in azioni e per il 10% in T-bills o debito a breve termine, utilizzati come collaterale per i contratti futures obbligazionari.

L'idea alla base del 90/60 è di sfruttare la capital efficiency, cioè l'uso efficiente del capitale, e quindi la leva finanziaria, per sfondare il muro del 100% e diversificare il portafoglio senza sacrificare la crescita dovuta alla parte azionaria.
Negli Stati Uniti, l'ETF NTSX replica questa strategia dal 20..., mentre il "gemello" UCITS NTSG, con qualche spiacevole variazione, fa lo stesso per gli investitori retail europei da qualche anno dopo.

I dettagli tecnici sulla logica e sull'implementazione di questi prodotti sono nell'appendice, mentre la bibliografia è in coda.

---

L'idea dietro questa breve analisi è, _again_, capire se la Pareto superiority regge, cioè se il 90/60 è migliore senza peggiorare nessuna delle metriche considerate, e, nel caso, demistificare l'uso della leva togliendole l'aura di "speculazione". Più nello specifico, ho preso come riferimento NTSG e l'ho confrontato con un'allocazione 60/40 e una 100% azionaria.

Dal punto di vista teorico, tutto sembra facile: prendi tre ETF, compari tre metriche e il gioco è fatto. Peccato che NTSG abbia due anni di storia, non ci sia un unico ETF per il 60/40 e la lunghezza delle serie storiche disponibili vari anche tra i maggiori ETF equities all-world.

Per quanto riguarda i due benchmark, la soluzione è abbastanza immediata: una combinazione degli indici MSCI World net total return e FTSE WGBI Developed Markets total return, con le rispettive stime di TER (0.10 per le azioni, 0.05 per le obbligazioni), permette di replicare in modo abbastanza realistico un ETF 100% azionario e un portafoglio 60/40.

Per NTSG la faccenda è leggermente più complicata. In primis, l'ETF investe tramite contratti futures che, per loro natura, non hanno una serie di prezzi continua nel tempo, in quanto soggetti a scadenza e rolling, cioè alla sostituzione dei contratti in scadenza. Esistono delle serie storiche "aggiustate" che riconciliano il divario tra un contratto e l'altro alla scadenza, ma fare backtest su di esse comporta una serie di semplificazioni e l'omissione dei costi di transazione e di roll.
Secondariamente, NTSG ha una metodologia tutt'altro che semplice: oltre ad applicare un filtro ESG alla sua selezione di azioni, investe solo in contratti futures di [elenco paesi] e ribilancia le posizioni periodicamente nei mesi di [elenco mesi] o quando le allocazioni oltrepassano la soglia di tolleranza del []%.

Di conseguenza, sono inizialmente partito da un modello di replica abbastanza semplice:


per poi affinarlo incrementalmente per avvicinarmi il più possibile alla realtà.


Quello che ne risulta, più che una replica di NTSG, è tuttavia un generico 90/60, in cui sono ovviamente modellizzati i costi della leva e un costo aggiuntivo per il drag dei futures. Un modello più realistico richiederebbe infatti dati più granulari sui futures e informazioni più dettagliate sulla metodologia di NTSG... cose che purtroppo, a meno di lavorare in WisdomTree, restano difficili da ottenere.

Eseguendo un semplice backtest tra il 90/60 (in tre versioni diverse in base al costo del drag applicato), il 60/40 e il 100% equities, a partire dal 19**, i risultati parlano da soli:





