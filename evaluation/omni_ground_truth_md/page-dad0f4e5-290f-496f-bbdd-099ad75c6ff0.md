## HOMEOMORPHISMS OF THE PSEUDOARC

23

hence $ p{ \sqcap }_{{G}_{m}}q $ , as $ {\sqsupseteq}_{n}^{m} $ is $ \sqcap $ -preserving. Conversely, if $p{ \sqcap }_{{G}_{m}}q$ then we have $ r \in {G}_{m + 1} $ with $ p,q > r $ , as $\sqsupseteq_{{m + 1}}^{m} $ is edge-witnessing, showing that $ { \sqcap }_{{G}_{m}} \subseteq { \land }_{m} $ . Thus $ \mathbb{P} $ is a $ \mathbf{K} $ -poset that is $\mathbf{K}$-subabsorbing, by construction.    $\square$

### 3.3. Compatiblity. Throughout the rest of this section we assume that

(1) $ \mathrm{K} $ is a fixed subcategory of the graph category $ \mathrm{G} $ .

(2) $ \mathbb{P} $ is a $K$-regular $K$-subabsorbing $K$-poset.

In particular, $ \mathbb{P} $ is regular so $ \mathrm{S}\mathbb{P} $ is Hausdorff, by [BBV23, Corollary 2.40]. As $ \mathbf{K} $- morphisms are co-injective, each level $ {\mathbb{P}}_{n} $ is a minimal cap, by [BBV23, Proposition 1.21], which thus yields a minimal open cover $\{ {{p}_{\mathrm{S}} : p \in {\mathbb{P}}_{n}}\} $ of $\mathrm{S}\mathbb{P} $ , by [BBV23, Proposition 2.8]. In particular, $ {p}_{\mathrm{S}} \neq \empty$ , for all $ p \in \mathbb{P} $ , i.e. $ \mathbb{P}$ is also a prime $ \omega $-poset.

We are interested in continuous maps on $ \mathrm{S}\mathbb{P} $ that are compatible with the given subcategory $ \mathbf{K} $ . First, for any finite $ \sqsupset \subseteq \mathbb{P} \times \mathbb{P} $ , let $ { \sqsupset }^{\mathbf{C}} $ denote the basic open subset of $ {\mathbf{C}}_{\mathrm{{S}\mathbb{P}}}^{\mathrm{{S}\mathbb{P}}} $ corresponding to the open subset $ {\sqsupset }^{\mathbf{S}} $ of strong refiners defined in (2.3), i.e.

$$
$${ \sqsupset}^{\mathbf{C}}=\left\{{\phi\in{\mathbf{C}}_{\mathrm{{S}\mathbb{P}}}^{\mathrm{{S}\mathbb{P}}} :\sqsupset\subseteq{ \sqsupset}_{\phi}}\right\}=\left\{{\phi\in{\mathbf{C}}_{\mathrm{{S}\mathbb{P}}}^{\mathrm{{S}\mathbb{P}}} : \forall p,q\left( {q\sqsupset p \Rightarrow{q}_{\mathrm{S}} \supseteq\phi\left\lbrack\overline{{p}_{\mathrm{S}}}\right\rbrack}\right) }\right\}.$$
$$

Definition 3.14. The $ \mathbf{K} $ -compatible functions on $ \mathrm{S}\mathbb{P} $ are given by

$$
$${\mathbf{C}}_{\mathbf{K}} = \mathop{\bigcap }\limits_{{m \in  \omega }}\mathop{\bigcup }\limits_{{n \geq  m}}\mathop{\bigcup }\limits_{{\sqsupset  \in  {\mathbf{K}}_{n}^{m}}}{ \sqsupset  }^{\mathbf{C}} = \left\{  {\phi  \in  {\mathbf{C}}_{\mathbf{S}\mathbb{P}}^{\mathbf{S}\mathbb{P}} : \forall m \in  \omega \exists { \sqsupset  }  \in  {\mathbf{K}}_{n}^{m}\left( {{ \sqsupset  }  \subseteq  {{ \sqsupset  } }_{\phi }}\right) }\right\}  .$$
$$

Corollary 2.32 tells us that $ {\mathbf{C}}_{\mathbf{K}} $ has another basis consisting of open sets $ { \leftarrow }_{\mathbf{K}} $ , for relations $ \leftarrow \subseteq {\mathbb{P}}_{n} \times {\mathbb{P}}_{n} $ defined on levels of $ \mathbb{P} $ , where

$$
$${ \leftarrow  }_{\mathbf{K}} = { \leftarrow  }_{\mathbf{C}} \cap  {\mathbf{C}}_{\mathbf{K}} = \left\{  {\phi  \in  {\mathbf{C}}_{\mathbf{K}} : \phi  \subseteq  { \leftarrow  }_{\mathsf{S}}}\right\}  .$$
$$

However,many of these basic sets can be empty and our interest in $ \mathbf{K} $ -like relations stems from the fact that these are the only ones for which $ { \leftarrow }_{\mathrm{S}} $ can contain any $ \phi \in {\mathbf{C}}_{\mathbf{K}} $ . We can even revert to a relation below $ \leftarrow $ which not just $ \mathbf{K}$ -like but widely $\mathbf{K} $ -subfactorisable (note every widely $\mathbf{K}$ -subfactorisable $\leftarrow$ is $\mathbf{K}$ -like,by Lemma 3.8, as $ \mathbb{P} $ is $\mathbf{K}$ -subabsorbing).

Let us denote the widely $\mathbf{K}$-subfactorisable relations on any $G \in \mathbf{K}$ by

$$
$${G}^{\mathbf{K}} = \left\{  { \leftarrow   \subseteq  G \times  G : \forall \gtrdot   \in  {\mathbf{K}}_{H}^{G}\left( { \lessdot  \circ   \leftarrow   \circ   \gtrdot \text{ subfactors into some }{ \sqsupset  } ,\exists  \in  {\mathbf{K}}_{I}^{H}}\right) }\right\}  .$$
$$

Lemma 3.15. For any $ m,{m}^{\prime } \in \omega , \leftarrow \subseteq {\mathbb{P}}_{m} \times {\mathbb{P}}_{m},{ \leftarrow }^{\prime } \subseteq {\mathbb{P}}_{{m}^{\prime }} \times {\mathbb{P}}_{{m}^{\prime }} $ and $ \phi \in { \leftarrow }_{\mathbf{K}} \cap { \leftarrow }_{\mathbf{K}}^{\prime } $ , we have some $ n > \max \left( {m,{m}^{\prime }}\right) $ and $ \twoheadleftarrow \subseteq {\mathbb{P}}_{n}^{\mathbf{K}} $ with $ \phi \in { \twoheadleftarrow }_{\mathbf{K}}, \twoheadleftarrow \leq \leftarrow $ and $ \twoheadleftarrow \leq { \leftarrow }^{\prime } $

Proof. By Proposition 2.31,we have $ k > m $ with $ { \leftarrow }_{k}^{\phi }{ \vartriangleleft }_{k} \leftarrow $ and $ { \leftarrow }_{k}^{\phi }{ \vartriangleleft }_{k}{ \leftarrow }^{\prime } $ . By Proposition 3.11, we have $ \mathbb{P} $ -subamalgamable $ \Rightarrow \in {\mathbf{K}}_{l}^{k} $ . As $ \phi \in {\mathbf{C}}_{\mathbf{K}} $ , we have $\sqsupset \in {\mathbf{K}}_{n}^{l} $ with $ \sqsupset\subseteq \sqsupset_{\phi } $ . By Propositions 2.19 and 2.36, $ \phi \subseteq {\left( \sqsupset \circ { \leq }_{n}^{l}\right) }_{\mathrm{S}} $ and $\sqsupset \circ { \leq }_{n}^{l} \subseteq { \leftarrow }_{l}^{\phi } $ . Now set

$$
$${ \twoheadleftarrow  }^{\prime } =  \lessdot  \circ      \gtrdot   \circ   \sqsupset   \circ  { \leq  }_{n}^{l} \circ   \lessdot  \circ      \gtrdot \;\text{ and }\; \twoheadleftarrow   = { \leq  }_{l}^{k} \circ    \gtrdot  \circ   \sqsupset   \circ  { \leq  }_{n}^{l} \circ   \lessdot    \circ  { \geq  }_{l}^{k}.$$
$$

As $  \sqsupset \circ { \leq }_{n}^{l} \subseteq { \twoheadleftarrow }^{\prime } $ , it follows that $ { \twoheadleftarrow }^{\prime } $ is also a $ \mathbf{K} $ -like relation satisfying $ \phi \subseteq { \twoheadleftarrow }_{\mathbf{S}}^{\prime } $ . The same then applies to the even larger relation $ \twoheadleftarrow $ , which is also widely $\mathbf{K} $ -subfactorisable, by Lemma 3.3. As $ \sqsupset \circ { \leq }_{n}^{l} \subseteq { \leftarrow }_{l}^{\phi } \subseteq { \leq }_{l}^{k} \circ { \leftarrow }_{k}^{\phi } \circ { \geq }_{l}^{k} $ and $ { \leftarrow }_{k}^{\phi }{ \vartriangleleft }_{k} \leftarrow $ ,

$\twoheadleftarrow \subseteq \leq^k_l \circ \geq^k_l \circ \leq^k_l \circ \leftarrow^{\phi}_k \circ \geq^k_l\circ\leq^k_l \circ \geq^k_l ~\subseteq ~\leq^k_l \circ\wedge_k \circ \leftarrow^{\phi}_k \circ \wedge_k \circ \geq^k_l ~\subseteq ~\leq^m_l \circ \leftarrow \circ \geq^m_l.$ This shows that $\twoheadleftarrow \leq \leftarrow$ and, likewise, $\twoheadleftarrow \leq {\leftarrow}^{\prime}$ as well.    □

Corollary 3.16. The open sets $ \left\{ {{ \leftarrow }_{\mathbf{K}} : n \in \omega ~\text{and} \leftarrow \in {\mathbb{P}}_{n}^{\mathbf{K}}}\right\} $ form a basis for $ {\mathbf{C}}_{\mathbf{K}} $ .

Proof. This is immediate from Lemma 3.15 once we note $ \twoheadleftarrow \leq \leftarrow $ implies $ { \twoheadleftarrow }_{\mathbf{K}} \subseteq { \leftarrow }_{\mathbf{K}} $ .
