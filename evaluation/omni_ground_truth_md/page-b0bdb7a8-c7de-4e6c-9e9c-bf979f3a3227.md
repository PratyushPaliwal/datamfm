## UNIVERSAL $\overline { { \partial } }$ SOLUTION ON STRONGLY PSEUDOCONVEX

9

Proof. By compactness of $ {b\Omega } $ we can take a finitely many ${\zeta }_{1},\ldots ,{\zeta }_{M} $ such that $ {b\Omega } \subset {\bigcup }_{{\nu = 1}}^{M}{\Phi }_{{\zeta }_{\nu }}\left( {U}_{{\zeta }_{\nu }}\right) $ . Let $ {\chi }_{0} \in {C}_{c}^{\infty }\left( \Omega \right) $and ${\chi }_{\nu } \in {C}_{c}^{\infty }\left( {{\Phi }_{{\zeta }_{\nu }}\left( {U}_{{\zeta }_{\nu }}\right) }\right) \left( {1 \leq \nu \leq M}\right) $be such that${\sum }_{{\nu = 0}}^{\infty }{\chi }_{\nu }\left( z\right) \equiv 1 $ for all $z \in \Omega $ . We take$ {\lambda }_{0} \in {C}_{c}^{\infty }\left( \Omega \right) $ and $ {\lambda }_{\nu } \in {C}_{c}^{\infty }\left( {{\Phi }_{{\zeta }_{\nu }}\left( {U}_{{\zeta }_{\nu }}\right) }\right) $ for $1 \leq \nu \leq M $, such that for each$ 0 \leq \nu \leq M,{\lambda }_{\nu } \equiv 1 $ in an open neighborhood of$ \operatorname{supp}{\chi }_{\nu } $ . Therefore $ {\chi }_{\nu } = {\lambda }_{\nu }{\chi }_{\nu } $ and $\operatorname{supp}{\chi }_{\nu } \cap \operatorname{supp}\left( {\overline{\partial }{\lambda }_{\nu }}\right) = \varnothing $ for$ 0 \leq \nu \leq M $ .

We need to apply Proposition 2.3. Set

$$
$${\mathscr{X}}_{q}^{k} \mathrel{\text{:=}} {H}^{k{t}_{0},2}\left( {\Omega ;{ \land  }^{0,q}}\right) ,\;0 \leq  q \leq  n,\;k \in  \mathbb{Z}.$$
$$

Therefore by Lemma A.13, we have ${\mathscr {X}}_{q}^{-\infty } = {\mathscr {S}}^{\prime }\left( {\Omega ;{ \land }^{0,q}}\right) $ and ${\mathscr {X}}_{q}^{+\infty } = {\mathscr {C}}^{\infty }\left( {\Omega ;{ \land }^{0,q}}\right) $ . Set $ {D}_{q} \mathrel{\text{:=}} \overline{\partial } $ on $(0,q)$-forms. Immediately (B) holds. By (2.4) we get (E).

We define operators ${P}^{\prime },{H}_{q}^{\prime } $ and$ {R}_{q}^{\prime } $on$ \Omega $ by the following:

$$
$${P}^{\prime }f \mathrel{\text{:=}} \mathop{\sum }\limits_{{\nu  = 1}}^{M}{\Phi }_{{\zeta }_{\nu } * }\left( {\left( {{\lambda }_{\nu } \circ  {\Phi }_{{\zeta }_{\nu }}}\right)  \cdot  {\mathcal{P}}^{{\zeta }_{\nu }}\left\lbrack  {{\Phi }_{{\zeta }_{\nu }}^{ * }\left( {{\chi }_{\nu }f}\right) }\right\rbrack  }\right)  = \mathop{\sum }\limits_{{\nu  = 1}}^{M}{\lambda }_{\nu } \cdot  {\Phi }_{{\zeta }_{\nu } * } \circ  {\mathcal{P}}^{{\zeta }_{\nu }} \circ  {\Phi }_{{\zeta }_{\nu }}^{ * }\left\lbrack  {{\chi }_{\nu }f}\right\rbrack  ;\tag{2.11}$$
$$

$$
$$H_q' f := \lambda_0 \cdot \mathcal{B}_q [\chi_0 f] + \sum_{\nu=1}^{M} \lambda_\nu \cdot \Phi_{\zeta_{\nu}*} \circ \mathcal{H}^{\zeta_\nu}_q\circ \Phi_{\zeta_\nu}^* [\chi_\nu f].\tag{2.12}$$
$$

Here$ {\mathcal{B}}_{q} $ are the Bochner-Martinelli integral operators from (A.23). Recall (see Lemmas A.29 and A.30) the boundedness$  {\mathcal{B}}_{q} : {H}_{c}^{s,2}\left( {\Omega ;{ \land }^{0,q}}\right) \rightarrow {H}^{s + 1,2}\left( {\Omega ;{ \land }^{0,q - 1}}\right) $ for all $ s \in \mathbb{R} $ and the formula $g = \bar{\partial }{\mathcal{B}}_{q}g + {\mathcal{B}}_{q + 1}\overline{\partial }g $ for$(0,q)$forms $g $that has compact support.

We define$ {\left( {R}_{q}\right) }_{q = 0}^{n} $ by $ {R}_{0}f \mathrel{\text{:=}} f - {P}^{\prime }f - {H}_{1}^{\prime }\bar{\partial }f $ and ${R}_{q}f \mathrel{\text{:=}} f - \overline{\partial }{H}_{q}^{\prime }f - {H}_{q + 1}^{\prime }\overline{\partial }f $for $1 \leq q \leq n $. Therefore (D) holds since we define$ {R}_{q} $ by this way.

To verify (C), we adapt the standard convention for forms of mixed degree from Convention 1.3: for form$  f = {\sum }_{{q = 0}}^{n}{f}_{q} $ where ${f}_{q} $ has degree$(0,q)$, we use$ {P}^{\prime }f = {P}^{\prime }{f}_{0} $ and $ {H}^{\prime }f = \mathop{\sum }\limits_{{q = 1}}^{n}{H}_{q}^{\prime }{f}_{q} $ and $ {Rf} = \mathop{\sum }\limits_{{q = 0}}^{n}{R}_{q}{f}_{q} $ . Therefore, $ {Rf} = f - {P}^{\prime }f - \overline{\partial }{H}^{\prime }f - {H}^{\prime }\overline{\partial }f $ , which means $\overline{\partial }R - R\overline{\partial } = \overline{\partial }{P}^{\prime } $ . Therefore (recall Remark 2.4 and we set $\left. {{R}_{n + 1} = 0}\right) $ ,

$$
$${R}_{q + 1}\overline{\partial } =\overline{\partial }{R}_{q}\;\text{ for }1 \leq  q \leq  n,\;\text{ and }\;{R}_{1}{\overline{\partial }}_{0} -\overline{\partial }{R}_{0} = \overline{\partial }{P}^{\prime }.$$
$$

Note that by (2.11) and (2.3) we have

$$
$$\overline{\partial }{P}^{\prime }f = \mathop{\sum }\limits_{{\nu  = 1}}^{M}\overline{\partial }{\lambda }_{\nu } \land  {\Phi }_{{\zeta }_{\nu } * }{\mathcal{P}}^{{\zeta }_{\nu }}\left\lbrack  {{\Phi }_{{\zeta }_{\nu }}^{ * }\left( {{\chi }_{\nu }f}\right) }\right\rbrack   = {\Phi }_{{\zeta }_{\nu } * } \circ  ( {( {{\Phi }_{{\zeta }_{\nu }}^{ * }\overline{\partial }{\lambda }_{\nu }})  \land  {\mathcal{P}}^{{\zeta }_{\nu }} \circ  \lbrack  {( {{\Phi }_{{\zeta }_{\nu }}^{ * }{\chi }_{\nu }})  \cdot  ( {{\Phi }_{{\zeta }_{\nu }}^{ * }f}) }\rbrack  }) .$$
$$

Since $\overline{\partial }{\lambda }_{\nu } $ and $ {\chi }_{\nu } $ have disjoint supports, so do$  {\Phi }_{{\zeta }_{\nu }}^{ * }\overline{\partial }{\lambda }_{\nu } $ and ${\Phi }_{{\zeta }_{\nu }}^{ * }{\chi }_{\nu } $ . By the assumption (c) we get $\overline{\partial }{P}^{\prime } $ : ${\mathscr {S}}^{\prime } \rightarrow {\mathscr {C}}^{\infty } $ . This completes the verification of (C).

To see $ {R}_{q} : {H}^{s,2} \rightarrow {H}^{s + {t}_{0},2} $ is bounded, i.e. to verify (A) we compute the explicit expression.

$$
$$Rf = f - P'f - \overline{\partial} H'f - H'\overline{\partial}f$$
$$

$$
$$= \lambda_0 \chi_0 f - \overline{\partial} (\lambda_0 \mathcal{B}[\chi_0 f]) - \lambda_0 \mathcal{B}[\chi_0 \overline{\partial}f]$$
$$

$$
$$+ \mathop{\sum }\limits_{{\nu  = 1}}^{M}\left\{  {{\lambda }_{\nu }{\chi }_{\nu }f - {\lambda }_{\nu }{\Phi }_{{\zeta }_{\nu } * }{\mathcal{P}}^{{\zeta }_{\nu }}{\Phi }_{{\zeta }_{\nu }}^{ * }\left\lbrack  {{\chi }_{\nu }f}\right\rbrack   - \overline{\partial }\left( {{\lambda }_{\nu }{\Phi }_{{\zeta }_{\nu } * }{\mathcal{H}}^{{\zeta }_{\nu }}{\Phi }_{{\zeta }_{\nu }}^{ * }\left\lbrack  {{\chi }_{\nu }f}\right\rbrack  }\right)  - {\lambda }_{\nu }{\Phi }_{{\zeta }_{\nu } * }{\mathcal{H}}^{{\zeta }_{\nu }}{\Phi }_{{\zeta }_{\nu }}^{ * }\lbrack  {{\chi }_{\nu }\overline{\partial }f}\rbrack }\right\}$$
$$

$$
$$= \lambda_0 \cdot ( \text{id}- \overline{\partial} \mathcal{B} - \mathcal{B} \overline{\partial})[\chi_0 f] - \overline{\partial} \lambda_0 \wedge \mathcal{B}[\chi_0 f] + \lambda_0 \cdot \mathcal{B}[\overline{\partial} \chi_0 \wedge f] + \sum_{\nu=1}^{M} \lambda_\nu \cdot \Phi_{\zeta_\nu*} \mathcal{H}^{\zeta_\nu} \Phi_{\zeta_\nu}^* [\overline{\partial} \chi_\nu \wedge f]$$
$$

$$
$$\quad + \sum_{\nu=1}^{M} \left\{ \lambda_\nu \cdot \Phi_{\zeta_\nu*} \left\{ \text{id}- \mathcal{P}^{\zeta_\nu} - \overline{\partial} \mathcal{H}^{\zeta_\nu} - \mathcal{H}^{\zeta_\nu} \overline{\partial} \right\} \Phi_{\zeta_\nu}^* [\chi_\nu f] - \overline{\partial} \lambda_\nu \wedge \Phi_{\zeta_\nu*} \mathcal{H}^{\zeta_\nu} \Phi_{\zeta_\nu}^* [\chi_\nu f] \right\}$$
$$

$$
$$= \lambda_0 \cdot \mathcal{B}[\overline{\partial} \chi_0 \wedge f] - \overline{\partial} \lambda_0 \wedge \mathcal{B}[\chi_0 f] + \sum_{\nu=1}^{M} \lambda_\nu \cdot \Phi_{\zeta_\nu*} \circ \mathcal{R}^{\zeta_\nu} \circ \Phi_{\zeta_\nu}^* [\chi_\nu f]$$
$$

$$
$$+ \sum_{\nu=1}^{M} \left\{ - \overline{\partial} \lambda_\nu \wedge \Phi_{\zeta_\nu*} \circ \mathcal{H}^{\zeta_\nu} \circ \Phi_{\zeta_\nu}^* [\chi_\nu f] + \lambda_\nu \cdot \Phi_{\zeta_\nu*} \circ \mathcal{H}^{\zeta_\nu} \circ \Phi_{\zeta_\nu}^* [\overline{\partial} \chi_\nu \wedge f] \right\}.$$
$$
