27

This model in [35] is equivalent to our construction when the sign is flipped. Notice that

$$
$${U}_{i} = {Z}_{{8i} + 1}{Z}_{{8i} + 3}{Z}_{{8i} + 5}{Z}_{{8i} + 7}$$
$$

is a symmetric operator, we have

$$
$$\left( {-\mathop{\sum }\limits_{I}{\widetilde{P}}_{I,I + 1}}\right) \mathop{\prod }\limits_{{i = 1}}^{\left\lbrack  L/8\right\rbrack  }{U}_{i} = \left\{  \begin{array}{ll} \mathop{\prod }\limits_{{i = 1}}^{\left\lbrack  L/8\right\rbrack  }{U}_{i}\left( {-\mathop{\sum }\limits_{I}{P}_{I,I + 1}}\right) & L \equiv  0{\;\operatorname{mod}\;8} \\  \mathop{\prod }\limits_{{i = 1}}^{\left\lbrack  L/8\right\rbrack  }{U}_{i}\left( {-\mathop{\sum }\limits_{I}{P}_{I,I + 1} - {\bar{P}}_{L/4 - 1,L/4} - {\bar{P}}_{L/4,L/4 + 1}}\right) & L \equiv  4{\;\operatorname{mod}\;8} \end{array}\right.$$
$$

where

$$
$$P_{I,I+1} = \frac{1}{4}(1 + Z_{4I-3} X_{4I-1} Z_{4I+1})(1 + Z_{4I-1} X_{4I+1} Z_{4I+3}),$$
$$

$$
$$\bar{P}_{L/4-1,L/4} = \frac{1}{4}(1 + Z_{L-7} X_{L-5} Z_{L-3})(1 - Z_{L-5} X_{L-3} Z_{L-1}),$$
$$

$$
$$\bar{P}_{L/4,1} = \frac{1}{4}(1 - Z_{L-3} X_{L-1} Z_1)(1 + Z_{L-1} X_1 Z_3).$$
$$

Thus the local projector is$ {P}_{I,I + 1} $ with exceptions on the boundary, which correspond to local symmetric defects. Since a phase is at the thermodynamic limit, the phase realized in [35] is equivalent to

$$
$$H =  - \mathop{\sum }\limits_{I}{P}_{I,I + 1}.$$
$$

The component of$  {P}_{I,I + 1} $ in each sector can be expanded as

$$
$$P_e = \frac{1}{4} 
\begin{array}{c|cccc}
 & ee & ss & r^2r^2 & sr^2sr^2 \\
\hline
ee & 1 & 1 & -1 & 1 \\
ss & 1 & 1 & -1 & 1 \\
r^2r^2 & -1 & -1 & 1 & -1 \\
sr^2sr^2 & 1 & 1 & -1 & 1 \\
\end{array},
P_s = \frac{1}{4} 
\begin{array}{c|cccc}
 & es & se & sr^2r^2 & r^2sr^2 \\
\hline
es & 1 & 1 & -1 & 1 \\
se & 1 & 1 & -1 & 1 \\
sr^2r^2 & -1 & -1 & 1 & -1 \\
r^2sr^2 & 1 & 1 & -1 & 1 \\
\end{array},$$
$$

$$
$$P_{r^2} = \frac{1}{4} 
\begin{array}{c|cccc}
 & e~r^2 & r^2~e & s~sr^2 & sr^2s \\
\hline
er^2 & 1 & 1 & 1 & -1 \\
r^2e & 1 & 1 & 1 & -1 \\
s~sr^2 & 1 & 1 & 1 & -1 \\
sr^2s & -1 & -1 & -1 & 1 \\
\end{array},
\quad
P_{sr^2} = \frac{1}{4} 
\begin{array}{c|cccc}
 & esr^2 & sr^2e & sr^2 & r^2s \\
\hline
esr^2 & 1 & 1 & 1 & -1 \\
sr^2e & 1 & 1 & 1 & -1 \\
s~r^2 & 1 & 1 & 1 & -1 \\
r^2s & -1 & -1 & -1 & 1 \\
\end{array}$$
$$

Define

$$
$$m_e = 
\begin{array}{c|cccc}
 & ee & ss & r^2r^2 & sr^2sr^2 \\
\hline
e & 1 & 1 & -1 & 1 \\
\end{array},
\quad
m_s = 
\begin{array}{c|cccc}
 & es & se & sr^2r^2 & r^2sr^2 \\
\hline
s & 1 & 1 & -1 & 1 \\
\end{array},$$
$$

$$
$$m_{r^2} = 
\begin{array}{c|cccc}
 & er^2 & r^2e & s~sr^2 & sr^2s \\
\hline
r^2 & 1 & 1 & 1 & -1 \\
\end{array},
\quad
m_{sr^2} = 
\begin{array}{c|cccc}
 & esr^2 & sr^2e & sr^2 & r^2s \\
\hline
sr^2 & 1 & 1 & 1 & -1 \\
\end{array}.$$
$$

Then

$$
$$P = \frac{1}{4}{m}^{ \dagger  }m.$$
$$

We can then extract the cocycle gauge by $m$:

$$
$$\omega \left( {{r}^{2},{r}^{2}}\right)  = \omega \left( {s{r}^{2},{r}^{2}}\right)  = \omega \left( {{r}^{2},s}\right)  = \omega \left( {s{r}^{2},s}\right)  =  - 1,\;\omega \left( \text{ others }\right)  = 1.$$
$$

Thus the Hamiltonian of [35], for either $ L = 0{\;\operatorname{mod}\;8} $ or $ L = 4{\;\operatorname{mod}\;8} $, matches our model locally

$$
$$H =  - \frac{1}{4}\mathop{\sum }\limits_{i}{m}_{i,i + 1}^{ \dagger  }{m}_{i,i + 1}.$$
$$

And the MPO ${A}_{\sigma } $acts on ground state as $\operatorname{Tr}\left( {A}_{\sigma }\right) \left| {e\rangle = 2}\right| e\rangle $ .

The third model is constructed similarly. After applying the CZ gate, the ground state is stabilized by the generator

$$
$$- {X}_{{2n} - 1} = 1,\; - {Z}_{{2n} - 2}{X}_{2n}{Z}_{{2n} + 2} = 1.$$
$$
