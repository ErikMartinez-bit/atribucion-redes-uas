# Formulación Matemática Formal: Modelo de Atribución UAS

## 1. Definición de la Red como Dígrafo

Se define la infraestructura de red de mando y control como un grafo dirigido no ponderado $G = (V, E)$, donde:

* $V$ representa el conjunto finito de nodos de la red, segmentado en tres subconjuntos disjuntos:

$$V = C \cup R \cup D \quad \text{con} \quad C \cap R = \emptyset, \; R \cap D = \emptyset, \; C \cap D = \emptyset$$

* $C$: Nodos Controladores (Operadores primarios / Fuentes emisoras).
* $R$: Nodos Repetidores / Relays terrestres o aéreos.
* $D$: Nodos Drones receptores de la señal.
* $E \subseteq V \times V$ representa el conjunto de aristas dirigidas (enlaces de comunicación RF), donde un par ordenado $(u, v) \in E$ indica que el nodo $u$ transmite órdenes o señales de control directamente al nodo $v$.

---

## 2. Definición Topológica del Emisor Primario (Nodo Origen)

Dado un nodo emisor $v \in V$, sus propiedades de grado en el dígrafo $G$ se definen formalmente como:

* **Grado de entrada ($d^-$):** $d^-(v) = |\{u \in V \mid (u, v) \in E\}|$
* **Grado de salida ($d^+$):** $d^+(v) = |\{w \in V \mid (v, w) \in E\}|$

### Criterio Base de Atribución:

Un nodo $v \in V$ se clasifica como un **Emisor Primario / Operador Raíz** si cumple estrictamente:

$$v \in C \iff d^-(v) = 0 \quad \land \quad d^+(v) > 0$$

Todo nodo intermediario $r \in R$ satisface $d^-(r) \ge 1$ y $d^+(r) \ge 1$. Todo nodo dron receptor $d \in D$ satisface $d^-(d) \ge 1$ y $d^+(d) = 0$.

---

## 3. Representación Matricial y Trazabilidad Inversa

### Representación Matricial

El dígrafo se representa computacionalmente mediante la matriz de adyacencia $A$ de dimensión $n \times n$ (donde $n = |V|$), tal que:

$$A_{ij} = \begin{cases} 1 & \text{si } (v_i, v_j) \in E \\ 0 & \text{en otro caso} \end{cases}$$

### El Grafo Transpuesto ($G^T$)

Para rastrear la trayectoria desde un dron objetivo interceptado $d_{target} \in D$ hacia su emisor primario, se define el **Grafo Transpuesto** $G^T = (V, E^T)$, donde:

$$E^T = \{(v, u) \mid (u, v) \in E\}$$

La inversión del sentido de los arcos $(u, v) \to (v, u)$ permite realizar una búsqueda de alcanzabilidad inversa (*backtracking*) desde $d_{target}$ en el subgrafo de ancestros $G_{sub}^T$. Dado que esta inversión es exacta sobre la totalidad de las aristas, toda trayectoria de longitud $k$ desde $d_{target}$ hasta un nodo $v$ en $G^T$ corresponde a una trayectoria de la misma longitud desde $v$ hasta $d_{target}$ en $G$; por lo tanto, la distancia hallada al recorrer $G^T$ desde $d_{target}$ equivale directamente a $d(v, d_{target})$ en el grafo original, sin necesidad de recorrer $G$ en su sentido natural.

---

## 4. Manejo de Ambigüedades y Casos Borde

Al ejecutar la búsqueda inversa sobre $G_{sub}^T$ pueden presentarse dos situaciones que se apartan del caso ideal de una única fuente identificable.

Puede ocurrir que se identifique un conjunto de candidatos con grado de entrada nulo $C_{candidatos} = \{v_1, v_2, \dots, v_k\}$ con $d^-(v_i) = 0$, en cuyo caso el emisor más probable se determina seleccionando aquel con el camino más corto hacia $d_{target}$:

$$C_{optimo} = \arg\min_{v \in C_{candidatos}} d(v, d_{target})$$

donde $d(u, v)$ representa la longitud del camino mínimo desde $u$ hasta $v$ en el dígrafo original $G$. Alternativamente, si la red se encuentra desconectada, los datos de origen son incompletos, o el dron objetivo quedó aislado sin una ruta de retorno hacia ningún nodo raíz, el conjunto de candidatos puede resultar vacío:

$$C_{candidatos} = \emptyset \implies \text{atribución no determinable}$$

En este escenario el algoritmo debe reportar explícitamente la imposibilidad de atribución en lugar de asumir un origen por defecto, preservando así la validez del modelo incluso ante datos de red imperfectos.

---

## 5. Complejidad Computacional

* **Transposición del Grafo:** La construcción de $G^T$ a partir de $G$ requiere invertir las $|E|$ aristas, tomando tiempo $\mathcal{O}(|V| + |E|)$.
* **Búsqueda en Anchura (BFS Inverse):** El recorrido desde $d_{target}$ en $G^T$ explora los vértices y aristas alcanzables en tiempo $\mathcal{O}(|V| + |E|)$.
* **Complejidad Total del Algoritmo:** $\mathcal{O}(|V| + |E|)$, lo que garantiza una ejecución eficiente para topologías de red en tiempo real.
