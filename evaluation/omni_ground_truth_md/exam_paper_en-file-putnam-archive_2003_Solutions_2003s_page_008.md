where

$$
$$
\begin{array}{l}
C_j = \#\{i < j : \mathrm{sgn}(a_i) = \mathrm{sgn}(a_j)\} \\
\qquad - \#\{i < j : \mathrm{sgn}(a_i) \neq \mathrm{sgn}(a_j)\}.
\end{array}
$$
$$

Consider the partial sum $P_k = \sum_{j=1}^k C_j$. If exactly $p_k$ of $a_1, \ldots, a_k$ are positive, then this sum is equal to

$$
$$
\binom{p_k}{2} + \binom{k-p_k}{2} - \left[ \binom{k}{2} - \binom{p_k}{2} - \binom{k-p_k}{2} \right],
$$
$$

which expands and simplifies to

$$
$$ -2p_k(k-p_k) + \binom{k}{2}. $$
$$

For $k \le 2p$ even, this partial sum would be minimized
with $p_k = \frac{k}{2}$, and would then equal $-\frac{k}{2}$; for $k < 2p$ odd,
this partial sum would be minimized with $p_k = \frac{k \pm 1}{2}$, and
would then equal $-\frac{k-1}{2}$. Either way, $P_k \ge -\lfloor \frac{k}{2} \rfloor$. On the
other hand, if $k > 2p$, then

$$
$$-2 p_{k}(k-p_{k})+\binom{k}{2} \geq-2 p(k-p)+\binom{k}{2}$$
$$

since $p_k$ is at most $p$. Define $Q_k$ to be $-\lfloor \frac{k}{2} \rfloor$ if $k \leq 2p$ and $-2p(k-p) + \binom{k}{2}$ if $k \geq 2p$, so that $P_k \geq Q_k$. Note that $Q_1 = 0$.

Partial summation gives

$$
$$
\begin{array}{l}
 \sum_{j=1}^{n} r_{j} C_{j}=r_{n} P_{n}+\sum_{j=2}^{n}\left(r_{j-1}-r_{j}\right) P_{j-1} \\
\qquad  \geq r_{n} Q_{n}+\sum_{j=2}^{n}\left(r_{j-1}-r_{j}\right) Q_{j-1} \\
\qquad  =\sum_{j=2}^{n} r_{j}\left(Q_{j}-Q_{j-1}\right) \\
\qquad  =-r_{2}-r_{4}-\cdots-r_{2 p}+\sum_{j=2 p+1}^{n}(j-1-2 p) r_{j} .
\end{array}
$$
$$

It follows that

$$
$$
\begin{align*}
\sum_{1 \le i < j \le n} |a_i + a_j| &= \sum_{i=1}^n (n-i)r_i + \sum_{j=1}^n r_j C_j \\
&\ge \sum_{i=1}^{2p} (n-i-[i \text{ even}]) r_i \\
&\qquad + \sum_{i=2p+1}^n (n-1-2p) r_i \\
&= (n-1-2p) \sum_{i=1}^n r_i \\
&\qquad + \sum_{i=1}^{2p} (2p+1-i-[i \text{ even}]) r_i \\
&\ge (n-1-2p) \sum_{i=1}^n r_i + p \sum_{i=1}^{2p} r_i \\
&\ge (n-1-2p) \sum_{i=1}^n r_i + p \frac{2p}{n} \sum_{i=1}^n r_i,
\end{align*}
$$
$$

as desired. The next-to-last and last inequalities each
follow from the monotonicity of the $r_i$'s, the former by
pairing the $i^{\mathrm{th}}$ term with the $(2p + 1 - i)^{\mathrm{th}}$.

Note: Compare the closely related Problem 6 from the 2000 USA Mathematical Olympiad: prove that for any nonnegative real numbers $a_1, \dots, a_n, b_1, \dots, b_n$, one has

$$
$$
\sum_{i,j=1}^{n} \min\{a_{i}a_{j}, b_{i}b_{j}\} \leq \sum_{i,j=1}^{n} \min\{a_{i}b_{j}, a_{j}b_{i}\}.
$$
$$

8
