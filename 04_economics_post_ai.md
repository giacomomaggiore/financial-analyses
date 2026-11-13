
## Scelta di formazione e tipi di agente

Consideriamo un'economia composta da $N$ agenti e due periodi, $t=0,1$. Al tempo $t=0$, ogni agente sceglie se acquisire una formazione specialistica:

$$
s_i\in\{0,1\},
$$

dove $s_i=1$ indica che l'agente studia. La formazione costa $\kappa_i>0$. Il costo è eterogeneo e distribuito nella popolazione secondo:

$$
\kappa_i\sim G(\kappa).
$$

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

Sia $c_i$ il consumo di beni essenziali, $x_i$ il consumo di beni discrezionali e $\bar c$ il livello minimo di sussistenza. In ciascun periodo gli agenti hanno preferenze Stone-Geary:

$$
u(c_i,x_i)=\beta\ln(c_i-\bar c)+(1-\beta)\ln(x_i).
$$

La funzione di utilità indiretta associata a un reddito disponibile $m$ è:

$$
v(m)=\ln(m-p_c\bar c)+C,
$$

dove $C$ è costante rispetto a $m$ e la soluzione richiede $m>p_c\bar c$. Con fattore di sconto $\eta\in(0,1)$, l'agente sceglie la formazione massimizzando:

$$
V_i(s_i)=v(m_{i,0})+\eta v(m_{i,1}).
$$

In particolare, studia se e solo se:

$$
\ln(B_0+D_{i,0}-\kappa_i-p_c\bar c)
-\ln(B_0+D_{i,0}-p_c\bar c)
+\eta\left[
\ln(m_{i,1}^{E}-p_c\bar c)
-\ln(m_{i,1}^{U}-p_c\bar c)
\right]\geq0.
$$

Il lavoro specialistico totale al tempo $t=1$ è quindi endogeno:

$$
L=\sum_{i=1}^{N}s_i.
$$

Nel seguito si omette l'indice temporale $t=1$. Nella prima sezione si assume proprietà privata egualitaria, quindi $D_i=D$.

Per l'agente $U$:

$$
\begin{aligned}
\max_{c_U,x_U}\quad
& \beta\ln(c_U-\bar c)+(1-\beta)\ln(x_U) \\
\text{soggetto a}\quad
& p_c c_U+p_x x_U\leq B+D, \\
& c_U>\bar c, \qquad x_U>0.
\end{aligned}
$$

Per l'agente $E$:

$$
\begin{aligned}
\max_{c_E,x_E}\quad
& \beta\ln(c_E-\bar c)+(1-\beta)\ln(x_E) \\
\text{soggetto a}\quad
& p_c c_E+p_x x_E\leq B+D+(1-\tau_w)w, \\
& c_E>\bar c, \qquad x_E>0.
\end{aligned}
$$

Affinché anche un non occupato superi la sussistenza:

$$
B+D>p_c\bar c.
$$

## Imprese, produzione e proprietà

La produzione avviene tramite capitale/AI $K$ e lavoro umano non automatizzabile $L$, fornito dagli agenti $E$:

$$
Y=F(K,L).
$$

Il capitale/AI è posseduto direttamente dagli azionisti dell'impresa: lo Stato possiede la quota $\gamma$ e i cittadini possiedono le quote $\theta_i$. Di conseguenza, il suo rendimento non è un pagamento separato $rK$ a soggetti esterni, ma confluisce nel flusso societario distribuibile agli azionisti.

Definiamo il surplus societario prima delle imposte e della distribuzione come:

$$
\pi=Y-wL-\delta K-I,
$$

dove $w$ è il salario lordo per unità di lavoro, $L$ è il lavoro totale impiegato, $\delta K$ è il costo di mantenimento e deprezzamento del capitale/AI e $I$ è l'investimento netto trattenuto per espandere il capitale.

Questa definizione chiude il bilancio dei redditi: salari e surplus societario sono interamente assegnati a lavoratori, cittadini o Stato. Il modello assume che l'AI generi rendite societarie positive. Con concorrenza perfetta, rendimenti di scala costanti e capitale remunerato separatamente al suo costo d'uso, varrebbe invece $Y=wL+rK$ e il profitto economico residuo sarebbe nullo.

La quota $\gamma\in[0,1]$ delle imprese è posseduta dallo Stato. La quota restante $1-\gamma$ è posseduta dai cittadini. Sia $\theta_i$ la quota di proprietà posseduta dal cittadino $i$; allora:

$$
\sum_i \theta_i=1-\gamma.
$$

Con proprietà egualitaria e una popolazione composta da $N$ cittadini:

$$
\theta_i=\frac{1-\gamma}{N}.
$$

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

In questa prima sezione assumiamo che la proprietà privata sia egualitaria. Ogni cittadino riceve quindi:

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

Il problema di ottimizzazione dell'agente generico è:

$$
\begin{aligned}
\max_{c_i,x_i}\quad
& \beta\ln(c_i-\bar c)+(1-\beta)\ln(x_i) \\
\text{soggetto a}\quad
& p_c c_i+p_x x_i\leq m_i, \\
& c_i>\bar c, \qquad x_i>0.
\end{aligned}
$$

Poiché l'utilità è crescente in entrambi i beni, il vincolo di bilancio è soddisfatto con uguaglianza. La Lagrangiana è:

$$
\mathcal{L}_i=
\beta\ln(c_i-\bar c)+(1-\beta)\ln(x_i)
+\lambda_i\left(m_i-p_c c_i-p_x x_i\right).
$$

Le condizioni del primo ordine sono:

$$
\frac{\beta}{c_i-\bar c}=\lambda_i p_c,
$$

$$
\frac{1-\beta}{x_i}=\lambda_i p_x,
$$

$$
p_c c_i+p_x x_i=m_i.
$$

Risolvendo il sistema, la domanda ottima dell'agente $i$ è:

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



Per $\tau_w$, i livelli ai due estremi sono:

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

Di conseguenza, se $\tau_w=1$, entrambi i gruppi hanno lo stesso reddito disponibile e gli stessi consumi ottimali. Se $\tau_w=0$, la distanza nei consumi è massima. Il parametro $\beta$ stabilisce come il divario di reddito è ripartito tra beni essenziali e discrezionali.

L'irrilevanza di $\gamma$ e $\tau_\pi$ è una conseguenza dell'ipotesi del modello: ogni unità di profitto $\pi$ è interamente distribuita, direttamente come dividendo oppure indirettamente come UBI. Se una quota delle entrate pubbliche fosse destinata a investimenti, servizi pubblici o spesa amministrativa, $\gamma$ e $\tau_\pi$ avrebbero invece effetti sul consumo corrente.

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

Il consumo ottimo non cambia rispetto al caso $\gamma=0$: cambia il canale distributivo. Con $\gamma=0$, parte dei profitti arriva come dividendo privato $D$; con $\gamma=1$, tutti i profitti arrivano attraverso l'UBI $B$.

---

## Proprietà privata non egualitaria

Consideriamo ora il caso in cui la quota privata delle imprese non è distribuita in modo egualitario. Il cittadino $i$ possiede la quota $\theta_i\geq0$, con:

$$
\sum_{i=1}^{N}\theta_i=1-\gamma.
$$

Il dividendo individuale dipende dalla partecipazione azionaria:

$$
D_i=\theta_i(1-\tau_\pi)\pi.
$$

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

A differenza del caso di proprietà egualitaria, il consumo ottimo dipende ora da $\theta_i$: un cittadino con una maggiore partecipazione azionaria riceve un dividendo più alto e consuma di più.

### Derivate parziali dei consumi

Consideriamo ancora derivate parziali, trattando $\pi$, $w$ e $L$ come esogeni. Dal reddito disponibile si ottiene:

$$
\frac{\partial m_i}{\partial\gamma}
=\frac{(1-\tau_\pi)\pi}{N},
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
=\frac{\beta}{p_c}\frac{(1-\tau_\pi)\pi}{N},
\qquad
\frac{\partial x_i^*}{\partial\gamma}
=\frac{1-\beta}{p_x}\frac{(1-\tau_\pi)\pi}{N},
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

Le derivate rispetto a $\gamma$ sono calcolate mantenendo costante la quota $\theta_i$ dell'agente considerato: l'aumento della quota pubblica deve quindi ridurre le quote possedute dagli altri cittadini, affinché $\sum_i\theta_i=1-\gamma$ rimanga soddisfatto.

L'effetto di $\tau_\pi$ dipende dalla proprietà dell'agente. Se $\theta_i>(1-\gamma)/N$, l'agente possiede più della quota privata media e un aumento dell'imposta sui profitti riduce i suoi consumi. Se $\theta_i<(1-\gamma)/N$, l'aumento di $\tau_\pi$ aumenta i suoi consumi, poiché riceve più UBI di quanto perda in dividendi. Se $\theta_i=(1-\gamma)/N$, l'effetto è nullo: questo riproduce il caso di proprietà egualitaria.