Similarly,

$$
$$
\begin{array} { r l } & { S _ { 2 } =  \sum _ { c = 1 } ^ { \infty }  \sum _ { b = c + 1 } ^ { \infty } \frac { 2 ^ { b + c } - 2 ^ { b - c + 1 } } { 3 ^ { b } 5 ^ { c } } } \\ & { \quad =  \sum _ { c = 1 } ^ { \infty } \Bigg ( \left( \left( \frac { 2 } { 5 } \right) ^ { c } - \frac { 2 } { 1 0 ^ { c } } \right)  \sum _ { b = c + 1 } ^ { \infty } \left( \frac { 2 } { 3 } \right) ^ { b } \Bigg ) } \\ & { \quad =  \sum _ { c = 1 } ^ { \infty } \left( \left( \frac { 2 } { 5 } \right) ^ { c } - \frac { 2 } { 1 0 ^ { c } } \right) 3 \left( \frac { 2 } { 3 } \right) ^ { c + 1 } } \\ & { \quad =  \sum _ { c = 1 } ^ { \infty } \left( 2 \left( \frac { 4 } { 1 5 } \right) ^ { c } - 4 \left( \frac { 1 } { 1 5 } \right) ^ { c } \right) } \\ & { \quad =  \frac { 3 4 } { 7 7 } . } \end{array}
$$
$$

We conclude that $S = S_1 + S_2 = \frac{17}{21}$.

Second solution: Recall that the real numbers $a, b, c$
form the side lengths of a triangle if and only if

$$
$$
s - a , s - b , s - c > 0 \qquad s = \frac { a + b + c } { 2 } ,
$$
$$

and that if we put $x=2(s-a), y=2(s-b), z=2(s-c)$,

$$
$$
a= { \frac { y + z } { 2 } } , b = { \frac { z + x } { 2 } } , c = { \frac { x + y } { 2 } } .
$$
$$

To generate all integer triples $(a,b,c)$ which form the
side lengths of a triangle, we must also assume that
$x,y,z$ are either all even or all odd. We may therefore
write the original sum as

$$
$$
\sum _ { x , y , z > 0 ~{ \mathrm { o d d } } } \frac { 2 ^ { ( y + z ) / 2 } } { 3 ^ { ( z + x ) / 2 } 5 ^ { ( x + y ) / 2 } } + \sum _ { x , y , z > 0 ~{ \mathrm { e v e n } } } \frac { 2 ^ { ( y + z ) / 2 } } { 3 ^ { ( z + x ) / 2 } 5 ^ { ( x + y ) / 2 } } .
$$
$$

To unify the two sums, we substitute in the first case
$x = 2u + 1$, $y = 2v + 1$, $z = 2w + 1$ and in the second
case $x = 2u + 2$, $y = 2v + 2$, $z = 2w + 2$ to obtain

$$
$$
\begin{array} { r l } & { \quad  \sum _ { ( a , b , c ) \in T } \frac { 2 ^ { a } } { 3 ^ { b } 5 ^ { c } } =  \sum _ { u , \nu , w = 1 } ^ { \infty } \frac { 2 ^ { \nu + w } } { 3 ^ { w + u } 5 ^ { u + \nu } } \left( 1 + \frac { 2 ^ { - 1 } } { 3 ^ { - 1 } 5 ^ { - 1 } } \right) } \\ & { \qquad  = \frac { 1 7 } { 2 } \sum _ { u = 1 } ^ { \infty } \left( \frac { 1 } { 1 5 } \right) ^ { u } \sum _ { \nu = 1 } ^ { \infty } \left( \frac { 2 } { 5 } \right) ^ { \nu } \sum _ { w = 1 } ^ { \infty } \left( \frac { 2 } { 3 } \right) ^ { w } } \\ & { \qquad  = \frac { 1 7 } { 2 } \frac { 1 / 1 5 } { 1 - 1 / 1 5 } \frac { 2 / 5 } { 1 - 2 / 5 } \frac { 2 / 3 } { 1 - 2 / 3 } } \\ & { \qquad  = \frac { 1 7 } { 2 1 } . } \end{array}
$$
$$

B5 The answer is 4.

Assume $n \ge 3$ for the moment. We write the permutations $\pi$ counted by $P_n$ as sequences $\pi(1),\pi(2),\ldots,\pi(n)$. Let $U_n$ be the number of permutations counted by $P_n$ that end with $n-1,n$; let $V_n$ be the number ending in $n,n-1$; let $W_n$ be the number starting with $n-1$ and ending in $n-2,n$; let $T_n$ be the number ending in $n-2,n$ but not starting with $n-1$; and let $S_n$

be the number which has $n-1,n$ consecutively in that
order, but not at the beginning or end. It is clear that
every permutation $\pi$ counted by $P_n$ either lies in exactly
one of the sets counted by $U_n, V_n, W_n, T_n, S_n$, or is the
reverse of such a permutation. Therefore

$$
$$
P _ { n } = 2 ( U _ { n } + V _ { n } + W _ { n } + T _ { n } + S _ { n } ) .
$$
$$

By examining how each of the elements in the sets
counted by $U_{n+1}, V_{n+1}, W_{n+1}, T_{n+1}, S_{n+1}$ can be obtained from a (unique) element in one of the sets
counted by $U_n, V_n, W_n, T_n, S_n$ by suitably inserting the element $n+1$, we obtain the recurrence relations

$$
$$
\begin{array} { r l } & { U _ { n + 1 } = U _ { n } + W _ { n } + T _ { n } , } \\ & { V _ { n + 1 } = U _ { n } , } \\ & { W _ { n + 1 } = W _ { n } , } \\ & { T _ { n + 1 } = V _ { n } , } \\ & { S _ { n + 1 } = S _ { n } + V _ { n } . } \end{array}
$$
$$

Also, it is clear that $W_n=1$ for all $n$.

So far we have assumed $n \geq 3$, but it is straightforward
to extrapolate the sequences $P_n, U_n, V_n, W_n, T_n, S_n$ back
to $n = 2$ to preserve the preceding identities. Hence for
all $n \geq 2$,

$$
$$
\begin{array} { r l }  P _ { n+ 5  } &= 2 (U_{ n + 5 }  +V_{ n + 5 } +W_{ n + 5 } + T_{ n+ 5 } + S_{ n+ 5 } )  \\ &= 2 ((U_{ n + 4}  +W_{ n + 4 } +T_{ n + 4 } + U_{ n+ 4 } \\ &\qquad {  + W_{ n+4 } + V_{ n+4 }+(S_{ n+ 4 }+V_{ n+4 } ) ) } \\ &= {  P _ { n+4 } + 2 ( U _ { n+4} + W _ { \ n+4 } + V _ {  n+4 } ) } \\ &= { P _ { n+4 } + 2 (( U_ { n+3} + W _ { \ n+3 } + T _ {  n+3 } ) +W _ { \ n+3 }+U _ { \ n+3 })} \\ &= {  P _ {n+4 } +  P _ {n+3 }+ 2( U _ {n+3 } -  V _ {n+3 } +  W _ {n+3 }- S _ {n+3 } ) } \\ &= {  P _ {n+4 } +  P _ {n+3 }+ 2((U _ {n+2 } + W _ {n+2 } + T _ {n+2 })- U _ {n+2 }  } \\ & \qquad+ {W _ {n+2}-(S_ {n+2}-V _ {n+2})) } \\ &= {  P _ {n+4 } +  P _ {n+3 }+ 2(2W _ {n+2 } + T _ {n+2 } - S _ {n+2 }- V _ {n+2 })  } \\ &= {  P _ {n+4 } +  P _ {n+3 }+ 2(2W _ {n+1} + V_ {n+1 } } \\ & { \qquad -( S _ {n+1 }+V _ {n+1} )-U_ {n+1})} \\ &= {  P _ {n+4 } +  P _ {n+3 }+ 2(2W_ {n } + U _ {n } - (S _ {n }+ V _ {n })-U_{n} } \\ & \qquad- {(U _ {n}+W_ {n}+T _ {n})) }\\&= {  P _ {n+4 } +  P _ {n+3 }-P_n+4} ,\end{array}
$$
$$

as desired.

Remark: There are many possible variants of the
above solution obtained by dividing the permutations
up according to different features. For example, Karl
Mahlburg suggests writing

$$
$$
P _ { n } = 2 P _ { n } ^ { \prime } , \qquad P _ { n } ^ { \prime } = Q _ { n } ^ { \prime } + R _ { n } ^ { \prime }
$$
$$

where $P_n'$ counts those permutations counted by $P_n$ for
which 1 occurs before 2, and $Q_n'$ counts those permutations counted by $P_n'$ for which $\pi(1) = 1$. One then has
the recursion

$$
$$
Q _ { n } ^ { \prime } = Q _ { n - 1 } ^ { \prime } + Q _ { n - 3 } ^ { \prime } + 1
$$
$$

6
