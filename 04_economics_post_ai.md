
## Scelta di formazione e tipi di agente

Consideriamo un'economia composta da $N$ agenti e due periodi, $t=0,1$. Al tempo $t=0$, ogni agente sceglie se acquisire una formazione specialistica:

$$
s_i\in\{0,1\},
$$

dove $s_i=1$ indica che l'agente studia. Il costo di formazione $\kappa_i>0$ è eterogeneo: i costi sono estratti indipendentemente da una normale troncata a zero,

$$
\kappa_i\sim\mathcal{N}(\mu_\kappa,\sigma_\kappa^2)\mid \kappa_i>0,
\qquad \sigma_\kappa>0.
$$

Indicando con $\Phi$ la funzione di ripartizione della normale standard, la funzione di ripartizione dei costi è:

$$
G(k)=\begin{cases}
0 & \text{se } k\leq0,\\
\displaystyle\frac{\Phi\left((k-\mu_\kappa)/\sigma_\kappa\right)-\Phi\left(-\mu_\kappa/\sigma_\kappa\right)}{1-\Phi\left(-\mu_\kappa/\sigma_\kappa\right)} & \text{se } k>0.
\end{cases}
$$

I costi sono indipendenti dalle quote di proprietà e dai redditi iniziali. Questa ipotesi riguarda le caratteristiche prima della scelta: non implica che costi e proprietà siano indipendenti tra gli agenti che scelgono di studiare.

Al tempo $t=0$, l'agente dispone di trasferimenti e dividendi iniziali e sostiene il costo della formazione:

$$
m_{i,0}=B_0+D_{i,0}-\kappa_i s_i.
$$

Al tempo $t=1$, la scelta determina il tipo dell'agente. Non introduciamo incertezza occupazionale: ogni agente formato ottiene un impiego specialistico.

- $U$: agente non formato, con $s_i=0$, non occupato;
- $E$: agente formato, con $s_i=1$, occupato in un lavoro ad alto valore aggiunto non automatizzabile.

Indicando inizialmente con $D_i$ il dividendo individuale, il reddito al tempo $t=1$ è:

$$
m_{i,1}=B_1+D_{i,1}+(1-\tau_w)w s_i.
$$

Sia $c_i$ il consumo di beni essenziali, $x_i$ il consumo di beni discrezionali e $\bar c$ il livello minimo di sussistenza. I prezzi $p_c,p_x>0$ sono uguali nei due periodi e $0<\beta<1$. In ciascun periodo gli agenti hanno preferenze Stone-Geary:

$$
u(c_i,x_i)=\beta\ln(c_i-\bar c)+(1-\beta)\ln(x_i).
$$

La funzione di utilità indiretta $v(m)$ è l'utilità massima raggiungibile con reddito disponibile $m$. L'agente risolve:

$$
\max_{c_i,x_i}\;\beta\ln(c_i-\bar c)+(1-\beta)\ln(x_i)
\quad\text{soggetto a}\quad p_c c_i+p_x x_i\leq m,
\qquad c_i>\bar c,\quad x_i>0.
$$

Poiché l'utilità aumenta con entrambi i consumi, il vincolo di bilancio è soddisfatto con uguaglianza. Le condizioni del primo ordine implicano:

$$
\frac{\beta}{p_c(c_i-\bar c)}
=\frac{1-\beta}{p_x x_i}.
$$

Ponendo $z=m-p_c\bar c>0$, la spesa oltre la sussistenza si divide quindi nelle proporzioni $\beta$ e $1-\beta$. Le scelte ottimali sono:

$$
c_i^*=\bar c+\frac{\beta z}{p_c},
\qquad
x_i^*=\frac{(1-\beta)z}{p_x}.
$$

Sostituendole nella funzione di utilità:

$$
\begin{aligned}
v(m)&=u(c_i^*,x_i^*) \\
&=\beta\ln\left(\frac{\beta z}{p_c}\right)
+(1-\beta)\ln\left(\frac{(1-\beta)z}{p_x}\right) \\
&=\ln(m-p_c\bar c)+C,
\end{aligned}
$$

con $C=\beta\ln(\beta/p_c)+(1-\beta)\ln((1-\beta)/p_x)$ costante rispetto a $m$. Con fattore di sconto $\eta\in(0,1)$, l'agente sceglie la formazione massimizzando:

$$
V_i(s_i)=v(m_{i,0})+\eta v(m_{i,1}).
$$

Se entrambe le scelte sono fattibili, studia se e solo se:

$$
\ln(B_0+D_{i,0}-\kappa_i-p_c\bar c)
-\ln(B_0+D_{i,0}-p_c\bar c)
+\eta\left[
\ln(m_{i,1}^{E}-p_c\bar c)
-\ln(m_{i,1}^{U}-p_c\bar c)
\right]\geq0.
$$

Se il reddito iniziale non consente di sostenere il costo mantenendo $m_{i,0}>p_c\bar c$, la formazione non è una scelta fattibile. Questo caso è possibile perché la distribuzione dei costi non è limitata superiormente.

Il lavoro specialistico totale al tempo $t=1$ è quindi endogeno:

$$
L=\sum_{i=1}^{N}s_i.
$$

Nel seguito si omette l'indice temporale $t=1$. Il caso generale assume proprietà privata non egualitaria: i dividendi $D_i$ possono differire tra cittadini. La proprietà egualitaria sarà considerata come caso particolare dopo la soluzione del modello.

Per un agente $i$, il reddito disponibile è $B+D_i$ se non è occupato e $B+D_i+(1-\tau_w)w$ se è occupato. Per una soluzione interna, il reddito di ciascun agente deve superare $p_c\bar c$.

## Imprese, produzione e proprietà

La produzione avviene tramite capitale/AI $K$ e lavoro umano non automatizzabile $L$, fornito dagli agenti $E$, secondo una funzione Cobb–Douglas:

$$
Y=F(K,L)=A K^\alpha L^{1-\alpha},
\qquad A>0,\quad K>0,\quad 0<\alpha<1.
$$

Assumiamo che il salario lordo sia pari alla produttività marginale del lavoro:

$$
w=\frac{\partial Y}{\partial L}
=(1-\alpha)A K^\alpha L^{-\alpha},\qquad L>0.
$$

Il salario dipende quindi dall'occupazione. Consideriamo soltanto equilibri con $L>0$: per $L=0$ la produzione è nulla, ma la produttività marginale e il salario non sono definiti. Il caso senza occupati richiederebbe una specificazione separata e non è incluso nella ricerca della politica ottimale.

Il capitale/AI è posseduto direttamente dagli azionisti dell'impresa: lo Stato possiede la quota $\gamma$ e i cittadini possiedono le quote $\theta_i$. Di conseguenza, il suo rendimento non è un pagamento separato $rK$ a soggetti esterni, ma confluisce nel flusso societario distribuibile agli azionisti.

Assumiamo che il capitale $K$ sia dato e che non vi siano investimenti né deprezzamento. Il surplus societario prima delle imposte e della distribuzione è:

$$
\pi=Y-wL,
$$

dove $w$ è il salario lordo per unità di lavoro e $L$ è il lavoro totale impiegato.

Con la Cobb–Douglas e il salario marginale, $wL=(1-\alpha)Y$ e quindi:

$$
\pi=\alpha A K^\alpha L^{1-\alpha}>0.
$$

Salari e surplus societario sono assegnati a lavoratori, cittadini o Stato. Il surplus include il rendimento del capitale posseduto dagli azionisti, non necessariamente un profitto economico puro. Con concorrenza perfetta, rendimenti di scala costanti e capitale remunerato separatamente al suo costo d'uso, varrebbe invece $Y=wL+rK$ e il profitto economico residuo sarebbe nullo.

La quota $\gamma\in[0,1]$ delle imprese è posseduta dallo Stato. La quota restante $1-\gamma$ è posseduta dai cittadini. Sia $\theta_i\geq0$ la quota di proprietà posseduta dal cittadino $i$; allora:

$$
\sum_{i=1}^{N}\theta_i=1-\gamma.
$$

Nel caso generale le quote $\theta_i$ possono essere diverse.

Con imposta societaria $\tau_\pi$, il profitto dopo imposte è:

$$
\pi^{net}=(1-\tau_\pi)\pi.
$$

Le entrate pubbliche totali sono composte da imposta sui profitti, dividendi della quota statale e imposta sui salari:

$$
R=\tau_\pi\pi+\underbrace{\gamma(1-\tau_\pi)\pi}_{\text{dividendi allo Stato}}+\underbrace{\tau_w wL}_{\text{imposta totale sui salari}}.
$$

Se tutte le entrate sono distribuite come UBI, il trasferimento individuale è:

$$
B=\frac{R}{N} = \frac{\tau_\pi\pi+\underbrace{\gamma(1-\tau_\pi)\pi}_{\text{dividendi allo Stato}}+\underbrace{\tau_w wL}_{\text{imposta totale sui salari}}}{N}.
$$

Il dividendo totale destinato ai cittadini corrisponde alla quota privata dei profitti:

$$
D^{tot}=(1-\gamma)(1-\tau_\pi)\pi.
$$

Il dividendo ricevuto dal cittadino $i$ è:

$$
D_i=\theta_i(1-\tau_\pi)\pi.
$$

---

## Soluzione del modello con proprietà privata non egualitaria

La partecipazione individuale $\theta_i$ determina il dividendo:

$$
D_i=\theta_i(1-\tau_\pi)\pi.
$$

In generale, cittadini diversi possiedono quote diverse e ricevono dividendi diversi.

L'UBI resta uguale per tutti, perché è finanziato dalle entrate pubbliche complessive:

$$
B=\frac{\tau_\pi\pi+\gamma(1-\tau_\pi)\pi+\tau_w wL}{N}.
$$

Definiamo ancora il salario lordo individuale:

$$
w_i=
\begin{cases}
0 & \text{se } i\in U,\\
w & \text{se } i\in E.
\end{cases}
$$

Il reddito disponibile dell'agente $i$ è:

$$
\begin{aligned}
m_i
&=B+D_i+(1-\tau_w)w_i \\
&=\frac{\tau_\pi\pi+\gamma(1-\tau_\pi)\pi+\tau_w wL}{N}
+\theta_i(1-\tau_\pi)\pi
+(1-\tau_w)w_i.
\end{aligned}
$$

Il problema di ottimizzazione dell'agente $i$ è:

$$
\begin{aligned}
\max_{c_i,x_i}\quad
& \beta\ln(c_i-\bar c)+(1-\beta)\ln(x_i) \\
\text{soggetto a}\quad
& p_c c_i+p_x x_i\leq m_i, \\
& c_i>\bar c, \qquad x_i>0.
\end{aligned}
$$

La Lagrangiana è:

$$
\mathcal{L}_i=
\beta\ln(c_i-\bar c)+(1-\beta)\ln(x_i)
+\lambda_i\left(m_i-p_c c_i-p_x x_i\right).
$$

Le condizioni del primo ordine sono:

$$
\frac{\beta}{c_i-\bar c}=\lambda_i p_c,
\qquad
\frac{1-\beta}{x_i}=\lambda_i p_x,
\qquad
p_c c_i+p_x x_i=m_i.
$$

La domanda ottima è:

$$
\begin{aligned}
c_i^*
&=\bar c+\frac{\beta}{p_c}\left(m_i-p_c\bar c\right) \\
&=\bar c+\frac{\beta}{p_c}\left[
\frac{\tau_\pi\pi+\gamma(1-\tau_\pi)\pi+\tau_w wL}{N}
+\theta_i(1-\tau_\pi)\pi
+(1-\tau_w)w_i-p_c\bar c
\right],
\end{aligned}
$$

$$
\begin{aligned}
x_i^*
&=\frac{1-\beta}{p_x}\left(m_i-p_c\bar c\right) \\
&=\frac{1-\beta}{p_x}\left[
\frac{\tau_\pi\pi+\gamma(1-\tau_\pi)\pi+\tau_w wL}{N}
+\theta_i(1-\tau_\pi)\pi
+(1-\tau_w)w_i-p_c\bar c
\right].
\end{aligned}
$$

La soluzione interna richiede:

$$
m_i>p_c\bar c.
$$

Il consumo ottimo dipende da $\theta_i$: a parità di reddito da lavoro, un cittadino con una partecipazione azionaria maggiore riceve un dividendo più alto e consuma di più.

### Derivate parziali dei consumi

Consideriamo derivate parziali, trattando $\pi$, $w$, $L$ e i prezzi come costanti. Per la derivata rispetto a $\gamma$ assumiamo che, per $\gamma<1$, le quote private si riducano proporzionalmente quando aumenta la quota pubblica:

$$
\frac{d\theta_i}{d\gamma}=-\frac{\theta_i}{1-\gamma}.
$$

Dal reddito disponibile si ottiene:

$$
\frac{\partial m_i}{\partial\gamma}
=(1-\tau_\pi)\pi\left(\frac{1}{N}-\frac{\theta_i}{1-\gamma}\right),
$$

$$
\frac{\partial m_i}{\partial\tau_\pi}
=\pi\left(\frac{1-\gamma}{N}-\theta_i\right),
$$

$$
\frac{\partial m_i}{\partial\tau_w}
=\frac{wL}{N}-w_i,
$$

$$
\frac{\partial m_i}{\partial\theta_i}
=(1-\tau_\pi)\pi.
$$

Di conseguenza:

$$
\frac{\partial c_i^*}{\partial\gamma}
=\frac{\beta}{p_c}(1-\tau_\pi)\pi\left(\frac{1}{N}-\frac{\theta_i}{1-\gamma}\right),
\qquad
\frac{\partial x_i^*}{\partial\gamma}
=\frac{1-\beta}{p_x}(1-\tau_\pi)\pi\left(\frac{1}{N}-\frac{\theta_i}{1-\gamma}\right),
$$

$$
\frac{\partial c_i^*}{\partial\tau_\pi}
=\frac{\beta\pi}{p_c}\left(\frac{1-\gamma}{N}-\theta_i\right),
\qquad
\frac{\partial x_i^*}{\partial\tau_\pi}
=\frac{(1-\beta)\pi}{p_x}\left(\frac{1-\gamma}{N}-\theta_i\right),
$$

$$
\frac{\partial c_i^*}{\partial\tau_w}
=\frac{\beta}{p_c}\left(\frac{wL}{N}-w_i\right),
\qquad
\frac{\partial x_i^*}{\partial\tau_w}
=\frac{1-\beta}{p_x}\left(\frac{wL}{N}-w_i\right),
$$

$$
\frac{\partial c_i^*}{\partial\theta_i}
=\frac{\beta}{p_c}(1-\tau_\pi)\pi,
\qquad
\frac{\partial x_i^*}{\partial\theta_i}
=\frac{1-\beta}{p_x}(1-\tau_\pi)\pi.
$$

Se $\tau_\pi<1$, un aumento di $\gamma$ redistribuisce i profitti dai cittadini con $\theta_i>(1-\gamma)/N$ a quelli con $\theta_i<(1-\gamma)/N$: la riduzione proporzionale dei dividendi privati è compensata da un UBI maggiore. L'effetto è nullo per chi possiede la quota media. A $\gamma=1$ le formule per le derivate rispetto a $\gamma$ non sono definite: il loro limite dipende dalla distribuzione delle quote prima che la proprietà diventi interamente pubblica. La derivata rispetto a $\theta_i$ descrive invece una variazione della quota individuale a $\gamma$ costante, compensata da variazioni delle quote degli altri cittadini.

Anche l'effetto di $\tau_\pi$ dipende dalla proprietà: un aumento dell'imposta riduce i consumi di chi possiede più della quota privata media e aumenta quelli di chi ne possiede meno. Se $\theta_i=(1-\gamma)/N$, l'effetto è nullo. A $\gamma=1$ non rimane proprietà privata e l'effetto di $\tau_\pi$ è nullo per tutti.

Per due cittadini $i$ e $j$, il divario di reddito e i corrispondenti divari di consumo sono:

$$
m_i-m_j=(1-\tau_\pi)\pi(\theta_i-\theta_j)+(1-\tau_w)(w_i-w_j),
$$

$$
c_i^*-c_j^*=\frac{\beta}{p_c}(m_i-m_j),
\qquad
x_i^*-x_j^*=\frac{1-\beta}{p_x}(m_i-m_j).
$$

Il divario riflette quindi sia la proprietà sia il lavoro. Nel confronto ipotetico a occupazione data, anche con $\tau_w=1$ differenze di proprietà possono lasciare redditi e consumi diversi; il confronto tra occupati e non occupati dipende inoltre dalla distribuzione delle quote nei due gruppi. Queste sono analisi parziali: se $L$, $w$ o $\pi$ cambiano in risposta alle politiche, gli effetti complessivi possono essere diversi.

### Scelta ottima di formazione

Assumiamo che ogni agente consideri dati i trasferimenti, i dividendi e il salario quando sceglie se studiare. Definiamo il reddito iniziale e quello futuro da non occupato al netto della spesa di sussistenza:

$$
A_i=B_0+D_{i,0}-p_c\bar c,
\qquad
H_i=B+D_i-p_c\bar c.
$$

Per $A_i>0$, $H_i>0$ e $(1-\tau_w)w\geq0$, la condizione iniziale per la formazione equivale a:

$$
s_i=1\quad\Longleftrightarrow\quad
\kappa_i\leq\kappa_i^*
=A_i\left[1-\left(\frac{H_i}{H_i+(1-\tau_w)w}\right)^\eta\right].
$$

A parità degli altri parametri, un dividendo futuro maggiore aumenta $H_i$ e riduce il beneficio relativo del salario, quindi riduce la soglia $\kappa_i^*$. Se il salario netto è nullo, anche la soglia è nulla e, poiché $\kappa_i>0$, nessuno studia. I dividendi iniziali influenzano invece la possibilità di sostenere il costo della formazione attraverso $A_i$.

Il lavoro aggregato deve essere coerente con le scelte individuali:

$$
L=\sum_{i=1}^{N}\mathbf{1}\!\left\{\kappa_i\leq\kappa_i^*\right\}.
$$

Questa è una condizione di equilibrio a punto fisso: il salario marginale, i profitti e l'UBI dipendono da $L$, che a sua volta dipende dalle scelte di formazione. L'indipendenza assunta separa la distribuzione dei costi da quella iniziale delle quote e dei redditi, ma queste ultime continuano a influenzare le soglie individuali. In una popolazione finita l'occupazione dipende anche dai costi effettivamente estratti; non si può sostituire automaticamente la condizione precedente con una somma di probabilità valutate a soglie determinate dall'equilibrio stesso.

Per calcolare un equilibrio occorrono i valori dei parametri, $K$, le quote, i redditi iniziali e le realizzazioni dei costi. Il modello non garantisce l'esistenza o l'unicità di un equilibrio ammissibile con $L>0$ e $\pi>0$. In particolare, con $\tau_w=1$ il salario netto è nullo e nessuno studia: tale politica non produce un equilibrio nell'insieme considerato.

---

## Benessere sociale e politica ottimale

Definiamo il benessere sociale come la somma delle utilità individuali nei due periodi, attribuendo lo stesso peso a ogni agente:

$$
W=\sum_{i=1}^{N}V_i(s_i)
=\sum_{i=1}^{N}\left[\ln(m_{i,0}-p_c\bar c)+\eta\ln(m_i-p_c\bar c)\right]+N(1+\eta)C.
$$

Come riferimento, consideriamo il caso in cui il decisore pubblico osserva le caratteristiche degli agenti, inclusi i costi, e sceglie $\gamma$, $\tau_\pi$ e $\tau_w$ prima delle scelte di formazione, con una politica annunciata credibile. Manteniamo dati i trasferimenti e i dividendi iniziali e consideriamo aliquote tra zero e uno. Quando cambia $\gamma$, le quote private variano proporzionalmente, come nelle derivate precedenti. Il problema è:

$$
\max_{\gamma,\tau_\pi,\tau_w\in[0,1]} W,
$$

soggetto al bilancio pubblico, al vincolo sulle quote di proprietà, alle scelte individuali di formazione, alla condizione di equilibrio per $L>0$, a $\pi>0$ e alla fattibilità $m_{i,0}>p_c\bar c$ e $m_i>p_c\bar c$ per ogni agente. Salari e profitti devono essere coerenti con l'equilibrio risultante. Sono ammissibili solo le politiche che producono un tale equilibrio; in particolare, $\tau_w=1$ è esclusa. Se esistono più equilibri, occorre specificare quale si realizza prima di confrontare le politiche.

### Effetti redistributivi a occupazione data

Per isolare la redistribuzione, manteniamo fissi $s_i$, $L$, $w$, $\pi$ e i prezzi. Definiamo l'utilità marginale del reddito futuro per l'agente $i$ come:

$$
q_i=\frac{1}{m_i-p_c\bar c}.
$$

Per $\gamma<1$, dalle derivate dei redditi segue:

$$
\frac{\partial W}{\partial\gamma}
=\eta(1-\tau_\pi)\pi\sum_{i=1}^{N}q_i\left(\frac{1}{N}-\frac{\theta_i}{1-\gamma}\right),
$$

$$
\frac{\partial W}{\partial\tau_\pi}
=\eta\pi\sum_{i=1}^{N}q_i\left(\frac{1-\gamma}{N}-\theta_i\right),
\qquad
\frac{\partial W}{\partial\tau_w}
=\eta\sum_{i=1}^{N}q_i\left(\frac{wL}{N}-w_i\right).
$$

A parità di occupazione e produzione, il decisore dovrebbe aumentare uno strumento se la rispettiva derivata è positiva e ridurlo se è negativa, rispettando i limiti ammessi. In particolare, aumentare la proprietà pubblica o l'imposta sui profitti accresce $W$ quando la redistribuzione sottrae reddito a cittadini con utilità marginale mediamente più bassa e lo trasferisce a cittadini con utilità marginale mediamente più alta. Lo stesso criterio vale per l'imposta salariale: il risultato dipende da come i redditi da lavoro sono distribuiti rispetto alle utilità marginali. Proprietà elevata e reddito elevato non coincidono necessariamente, quindi i segni non sono determinati in generale.

### Incentivi e scelta della politica

Le derivate precedenti non sono effetti complessivi: cambiare la politica può modificare le scelte di formazione, $L$, i salari e i profitti. In particolare, un'imposta salariale più alta redistribuisce reddito ma riduce il salario netto e può scoraggiare la formazione. Anche le politiche sui profitti possono influire sulla formazione attraverso i dividendi e l'UBI. Il decisore deve quindi confrontare $W$ negli equilibri generati dalle politiche ammissibili, tenendo conto sia della redistribuzione sia degli effetti su incentivi e produzione.

Con un numero finito di agenti, le scelte di formazione sono discrete: non è sufficiente porre uguali a zero le derivate parziali precedenti. Senza valori per i parametri, il capitale, le quote e i redditi iniziali, e senza conoscere le realizzazioni dei costi, non è possibile individuare aliquote o una quota pubblica ottimali. Se le politiche sono scelte prima di osservare i costi, occorre invece specificare il criterio di scelta, ad esempio il benessere atteso, e valutare gli equilibri per le diverse realizzazioni. L'esistenza di un massimo nell'insieme ammissibile non è garantita. Il confronto mantiene inoltre l'ipotesi che l'acquisizione delle quote pubbliche non abbia costi.

---

## Caso particolare: proprietà privata egualitaria

Poniamo ora $\theta_i=(1-\gamma)/N$ per ogni cittadino. Questo caso particolare si ottiene direttamente dalla soluzione generale: ogni cittadino riceve

$$
D_i=D=\frac{D^{tot}}{N}
=\frac{(1-\gamma)(1-\tau_\pi)\pi}{N}.
$$

Definiamo il salario lordo individuale come:

$$
w_i=
\begin{cases}
0 & \text{se } i\in U,\\
w & \text{se } i\in E.
\end{cases}
$$

Il reddito disponibile dell'agente $i$ è:

$$
m_i=B+D+(1-\tau_w)w_i.
$$

Sostituendo le espressioni di $B$ e $D$, otteniamo:

$$
m_i=
\frac{\tau_\pi\pi+\gamma(1-\tau_\pi)\pi+\tau_w wL}{N}
+\frac{(1-\gamma)(1-\tau_\pi)\pi}{N}
+(1-\tau_w)w_i.
$$

Sostituendo questo reddito nelle domande ottime già ricavate, otteniamo:

$$
\begin{aligned}
c_i^*
&=\bar c+\frac{\beta}{p_c}\left(m_i-p_c\bar c\right) 
=\bar c+\frac{\beta}{p_c}\left[
\frac{\tau_\pi\pi+\gamma(1-\tau_\pi)\pi+\tau_w wL}{N}
+\frac{(1-\gamma)(1-\tau_\pi)\pi}{N}
+(1-\tau_w)w_i-p_c\bar c
\right].
\end{aligned}
$$

$$
\begin{aligned}
x_i^*
&=\frac{1-\beta}{p_x}\left(m_i-p_c\bar c\right) 
=\frac{1-\beta}{p_x}\left[
\frac{\tau_\pi\pi+\gamma(1-\tau_\pi)\pi+\tau_w wL}{N}
+\frac{(1-\gamma)(1-\tau_\pi)\pi}{N}
+(1-\tau_w)w_i-p_c\bar c
\right].
\end{aligned}
$$

La soluzione richiede:

$$
m_i>p_c\bar c.
$$

Per l'agente non occupato si pone $w_i=0$; per l'agente occupato si pone $w_i=w$.

## Effetto di $\gamma$, $\tau_w$ e $\tau_\pi$

Consideriamo derivate parziali, trattando $\pi$, $w$ e $L$ come esogeni. Sostituendo $B$ e $D$ nel reddito disponibile, i termini relativi ai profitti si semplificano:

$$
\begin{aligned}
m_i
&=\frac{\tau_\pi\pi+\gamma(1-\tau_\pi)\pi+\tau_w wL}{N}
+\frac{(1-\gamma)(1-\tau_\pi)\pi}{N}
+(1-\tau_w)w_i \\
&=\frac{\pi}{N}+\frac{\tau_w wL}{N}+(1-\tau_w)w_i \\
&=\frac{\pi}{N}+w_i+\tau_w\left(\frac{wL}{N}-w_i\right).
\end{aligned}
$$

Quindi $m_i$, $c_i^*$ e $x_i^*$ non dipendono da $\gamma$ né da $\tau_\pi$:

$$
\frac{\partial c_i^*}{\partial\gamma}=0,
\qquad
\frac{\partial x_i^*}{\partial\gamma}=0,
\qquad
\frac{\partial c_i^*}{\partial\tau_\pi}=0,
\qquad
\frac{\partial x_i^*}{\partial\tau_\pi}=0.
$$

Le derivate rispetto all'imposta sul lavoro sono:

$$
\frac{\partial c_i^*}{\partial\tau_w}
=\frac{\beta}{p_c}\left(\frac{wL}{N}-w_i\right),
$$

$$
\frac{\partial x_i^*}{\partial\tau_w}
=\frac{1-\beta}{p_x}\left(\frac{wL}{N}-w_i\right).
$$



Per $\tau_w$, i livelli ai due estremi, mantenendo ipoteticamente fissi $L$, $w$ e $\pi$, sono:

$$
\lim_{\tau_w\to0}c_i^*
=\bar c+\frac{\beta}{p_c}\left(\frac{\pi}{N}+w_i-p_c\bar c\right),
$$

$$
\lim_{\tau_w\to1}c_i^*
=\bar c+\frac{\beta}{p_c}\left(\frac{\pi}{N}+\frac{wL}{N}-p_c\bar c\right),
$$

$$
\lim_{\tau_w\to0}x_i^*
=\frac{1-\beta}{p_x}\left(\frac{\pi}{N}+w_i-p_c\bar c\right),
$$

$$
\lim_{\tau_w\to1}x_i^*
=\frac{1-\beta}{p_x}\left(\frac{\pi}{N}+\frac{wL}{N}-p_c\bar c\right).
$$

## Interpretazione distributiva dell'imposta sul lavoro

Assumendo che ciascun occupato fornisca una unità di lavoro, si ha $L<N$ quando esistono non occupati. Per un agente occupato, $w_i=w$ e quindi:

$$
\frac{wL}{N}-w=w\left(\frac{L}{N}-1\right)<0.
$$

Un aumento di $\tau_w$ riduce pertanto $c_E^*$ e $x_E^*$. Per un agente non occupato, $w_i=0$ e:

$$
\frac{wL}{N}-w_i=\frac{wL}{N}>0.
$$

Un aumento di $\tau_w$ aumenta quindi $c_U^*$ e $x_U^*$, attraverso la redistribuzione delle imposte salariali nell'UBI.

La distanza nei consumi tra occupati e non occupati è:

$$
c_E^*-c_U^*=\frac{\beta}{p_c}(1-\tau_w)w,
$$

$$
x_E^*-x_U^*=\frac{1-\beta}{p_x}(1-\tau_w)w.
$$

Nel confronto a occupazione e salario fissati, con $\tau_w=1$ entrambi i gruppi hanno lo stesso reddito disponibile e gli stessi consumi ottimali; con $\tau_w=0$ la distanza nei consumi è massima. Il caso $\tau_w=1$ non è però un equilibrio ammissibile con $L>0$, perché nessuno sceglierebbe la formazione. Il parametro $\beta$ stabilisce come il divario di reddito è ripartito tra beni essenziali e discrezionali.

L'irrilevanza di $\gamma$ e $\tau_\pi$ è una conseguenza dell'ipotesi del modello: ogni unità di profitto $\pi$ è interamente distribuita, direttamente come dividendo oppure indirettamente come UBI. Se una quota delle entrate pubbliche fosse destinata a servizi pubblici o spesa amministrativa, $\gamma$ e $\tau_\pi$ avrebbero invece effetti sul consumo corrente.

In particolare, se lo Stato possiede l'intero capitale produttivo, $\gamma=1$, il dividendo privato è nullo:

$$
D^{tot}=(1-\gamma)(1-\tau_\pi)\pi=0.
$$

Tutti i profitti netti affluiscono allo Stato. Le entrate pubbliche e l'UBI individuale diventano:

$$
R=\tau_\pi\pi+(1-\tau_\pi)\pi+\tau_w wL
=\pi+\tau_w wL,
$$

$$
B=\frac{\pi+\tau_w wL}{N}.
$$

Il reddito disponibile è quindi:

$$
m_i=B+(1-\tau_w)w_i.
$$

Nel caso egualitario il consumo ottimo non cambia rispetto a $\gamma=0$: cambia il canale distributivo. Con $\gamma=0$, parte dei profitti arriva come dividendo privato $D$; con $\gamma=1$, tutti i profitti arrivano attraverso l'UBI $B$. Nel caso generale, invece, il passaggio alla proprietà pubblica redistribuisce i dividendi privati diseguali tramite l'UBI. Il confronto non include eventuali costi di acquisizione delle quote pubbliche.

### Confronto con la proprietà non egualitaria

A parità di $\pi$, $w$, $L$, prezzi e stato occupazionale del cittadino, l'UBI è lo stesso nei due casi. Indicando con gli apici $eq$ e $ne$ le due distribuzioni, la differenza individuale è:

$$
m_i^{eq}-m_i^{ne}
=(1-\tau_\pi)\pi\left(\frac{1-\gamma}{N}-\theta_i\right).
$$

Di conseguenza:

$$
c_i^{*,eq}-c_i^{*,ne}
=\frac{\beta}{p_c}(m_i^{eq}-m_i^{ne}),
\qquad
x_i^{*,eq}-x_i^{*,ne}
=\frac{1-\beta}{p_x}(m_i^{eq}-m_i^{ne}).
$$

Con proprietà egualitaria, chi aveva una quota inferiore alla media consuma di più e chi aveva una quota superiore consuma di meno. La somma delle differenze di reddito è zero: a parità delle altre grandezze, cambia la distribuzione dei profitti privati, non il loro ammontare totale. Il divario tra cittadini dipende solo dal salario netto e, nel confronto ipotetico a occupazione data, scompare per tutti se $\tau_w=1$.

Anche la scelta di formazione può cambiare. Se i redditi iniziali $A_i$ e il salario netto restano invariati, la proprietà egualitaria aumenta la soglia di formazione di chi aveva una quota privata superiore alla media e la riduce per chi ne aveva una inferiore, perché cambia il rispettivo reddito futuro da non occupato. L'effetto complessivo su $L$ non è determinato senza conoscere le realizzazioni dei costi, le quote e i redditi iniziali, anche assumendo l'indipendenza iniziale dei costi. Se la distribuzione iniziale dei dividendi cambia anch'essa, varia anche $A_i$ e questa conclusione individuale non è necessariamente valida. In equilibrio, variazioni di occupazione, salari e profitti possono modificare ulteriormente il confronto.
