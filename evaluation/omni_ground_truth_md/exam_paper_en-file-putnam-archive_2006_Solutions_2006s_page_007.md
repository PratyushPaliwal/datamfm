as desired.

Remark: The use of Cesaro's lemma above is the special case $b_n = n$ of the Cesaro-Stolz theorem: if $a_n, b_n$
are sequences such that $b_n$ is positive, strictly increasing, and unbounded, and

$$
$$
\lim_{n \to \infty} \frac{a_{n+1} - a_n}{b_{n+1} - b_n} = L,
$$
$$

then

$$
$$ \lim_{n \to \infty} \frac{a_n}{b_n} = L. $$
$$

Second solution: In this solution, rather than applying Taylor's theorem with remainder to $(1+x)^m$ for $1 < m < 2$ and $x > 0$, we only apply convexity to deduce that $(1+x)^m \ge 1+mx$. This gives

$$
$$
a_{n+1}^{(k+1)/k} - a_n^{(k+1)/k} \geq \frac{k+1}{k},
$$
$$

and so

$$
$$
a_{n}^{(k+1)/k} \geq \frac{k+1}{k} n+c
$$
$$

for some $c \in \mathbb{R}$. In particular,

$$
$$
\liminf_{n \to \infty} \frac{a_n^{(k+1)/k}}{n} \geq \frac{k+1}{k}
$$
$$

and so

$$
$$
\liminf_{n \to \infty} \frac{a_n}{n^{k/(k+1)}} \geq \left(\frac{k+1}{k}\right)^{k/(k+1)}.
$$
$$

But turning this around, the fact that

$$
$$
\begin{array}{l}
a_{n+1} - a_n \\
= a_n^{-1/k} \\
\leq \left( \frac{k+1}{k} \right)^{-1/(k+1)} n^{-1/(k+1)} (1+o(1)),
\end{array}
$$
$$

where $o(1)$ denotes a function tending to 0 as $n \to \infty$,
yields

$$
$$
\begin{array}{l}a_{n} \\ \leq\left(\frac{k+1}{k}\right)^{-1 /(k+1)} \sum_{i=1}^{n} i^{-1 /(k+1)}(1+o(1)) \\ =\frac{k+1}{k}\left(\frac{k+1}{k}\right)^{-1 /(k+1)} n^{k /(k+1)}(1+o(1)) \\ =\left(\frac{k+1}{k}\right)^{k /(k+1)} n^{k /(k+1)}(1+o(1)),\end{array}
$$
$$

so

$$
$$
\limsup_{n \to \infty} \frac{a_n}{n^{k/(k+1)}} \leq \left( \frac{k+1}{k} \right)^{k/(k+1)}
$$
$$

and this completes the proof.

Third solution: We argue that $a_{n} \to \infty$ as in the first
solution. Write $b_{n} = a_{n} - L n^{k/(k+1)}$, for a value of $L$ to
be determined later. We have

$$
$$
\begin{array}{l}
b_{n+1} \\
=b_{n}+a_{n}^{-1 / k}-L\left((n+1)^{k /(k+1)}-n^{k /(k+1)}\right) \\
=e_{1}+e_{2},
\end{array}
$$
$$

where

$$
$$
\begin{array}{c}e_1 = b_n + a_n^{-1/k} - L^{-1/k}n^{-1/(k+1)} \\e_2 = L((n+1)^{k/(k+1)} - n^{k/(k+1)}) \\ -L^{-1/k}n^{-1/(k+1)}.\end{array}
$$
$$

We first estimate $e_1$. For $-1 < m < 0$, by the convexity of $(1+x)^m$ and $(1+x)^{1-m}$, we have

$$
$$
\begin{array}{c}
1+m x \leq(1+x)^{m} \\
\leq 1+m x(1+x)^{m-1}.
\end{array}
$$
$$

Hence

$$
$$
\begin{array}{rl}
-\frac{1}{k} L^{-(k+1)/k} n^{-1} b_n & \le e_1 - b_n \\
& \le -\frac{1}{k} b_n a_n^{-(k+1)/k}.
\end{array}
$$
$$

Note that both bounds have sign opposite to $b_n$; moreover, by the bound $a_n = \Omega(n^{(k-1)/k})$, both bounds have
absolutely value strictly less than that of $b_n$ for $n$ sufficiently large. Consequently, for $n$ large,

$$
$$|e_1| \leq |b_n|.$$
$$

We now work on $e_{2}$. By Taylor’s theorem with remainder applied to $(1 + x)^{m}$ for $x > 0$ and $0 < m < 1$,

$$
$$
\begin{align*}
1+m x & \geq(1+x)^{m} \\
      & \geq 1+m x+\frac{m(m-1)}{2} x^{2}.
\end{align*}
$$
$$

The “main term” of $L((n+1)^{k/(k+1)} - n^{k/(k+1)})$
is $L\frac{k}{k+1}n^{-1/(k+1)}$. To make this coincide with
$L^{-1/k}n^{-1/(k+1)}$, we take

$$
$$
L = \left( \frac { k + 1 } { k } \right) ^ { k / ( k + 1 ) } .
$$
$$

We then find that

$$
$$
|e_2| = O(n^{-2}),
$$
$$

and because $b_{n+1} = e_{1} + e_{2}$, we have $|b_{n+1}| \leq |b_{n}| + |e_{2}|$. Hence

$$
$$
|b_n| = O\left(\sum_{i=1}^{n} i^{-2}\right) = O(1),
$$
$$

7
