$$
$$\sigma_* (\mathbf{E}) \leq \sup_{\|\mathbf{w}\|=1} \left\| \mathbb{E} [\mathbf{E} \mathbf{w} \mathbf{w}^\top \mathbf{E}^\top] \right\|^{\frac{1}{2}} \leq \max_{i \in [N]} \sup_{\|\mathbf{w}\|=1} \left\| \mathbb{E} [\mathbf{E}_{i,:} \mathbf{w} \mathbf{w}^\top \mathbf{E}_{i,:}^\top] \right\|^{\frac{1}{2}} \leq \widetilde{\sigma}, \tag{S.13}$$
$$

$$
$$R(\mathbf{E})= \left\| \max_{i \in [N], l \in [L]} \left\| \mathbf{E}_{i,S_l} \right\| \right\|_\infty \leq \sqrt{M} B.$$
$$

Then the first inequality in Lemma S.5 follows by plugging these conditions into Proposition 1 with$ t=c\log d$ with a sufficiently large constant $c$.

Similarly,  for the second and third inequalities we use

$$
$$\sigma \left( {\mathbf{E}}_{i, : }\right)  = \max \left\{  {{\|\mathbb{E}\left\lbrack  {\mathbf{E}}_{i, : }^{\top }{\mathbf{E}}_{i, : }\right\rbrack  \|}^{\frac{1}{2}},{\|\mathbb{E}\left\lbrack  {\mathbf{E}}_{i, : }{\mathbf{E}}_{i, : }^{\top }\right\rbrack \|}^{\frac{1}{2}}}\right\}   \leq  \max \{ \sigma \sqrt{J},\widetilde{\sigma }\}  = \sigma \sqrt{J},$$
$$

$$
$$v(\mathbf{E}_{i,:}) = \left\| \text{Cov}(\mathbf{E}_{i,:}) \right\|^{\frac{1}{2}} \leq \widetilde{\sigma}, \sigma_*(\mathbf{E}_{i,:}) \leq \widetilde{\sigma}, R(\mathbf{E}_{i,:}) \leq \sqrt{M} B,$$
$$

and

$$
$$\sigma \left( {\mathbf{E}}_{ : ,j}\right)  = \max \left\{  {{\|\mathbb{E}\left\lbrack  {\mathbf{E}}_{ : ,j}^{\top }{\mathbf{E}}_{ : ,j}\right\rbrack  \|}^{\frac{1}{2}},{\|\mathbb{E}\left\lbrack  {\mathbf{E}}_{ : ,j}{\mathbf{E}}_{ : ,j}^{\top }\right\rbrack  \|}^{\frac{1}{2}}}\right\}   \leq  \sigma \sqrt{N},$$
$$

$$
$$v(\mathbf{E}_{:,j}) \leq \sigma, \quad \sigma_*(\mathbf{E}_{:,j}) \leq \sigma, \quad R(\mathbf{E}_{:,j}) \leq B.$$
$$

Furthermore, for the fourth and fifth inequalities,

$$
$$\sigma \left( {\mathbf{{EV}}}^{ * }\right)  = \max \left\{  {{\|\mathbb{E}\left\lbrack  {\mathbf{{EV}}}^{ * }{\mathbf{V}}^{*\top }{\mathbf{E}}^{\top }\right\rbrack  \|}^{\frac{1}{2}},{\|\mathbb{E}\left\lbrack  {\mathbf{V}}^{*\top }{\mathbf{E}}^{\top }{\mathbf{{EV}}}^{ * }\right\rbrack  \|}^{\frac{1}{2}}}\right\}   \leq  \widetilde{\sigma }\sqrt{N},$$
$$

$$
$$v(\mathbf{E} \mathbf{V}^*) \leq \widetilde{\sigma}, \quad \sigma_*(\mathbf{E} \mathbf{V}^*) \leq \sigma_*(\mathbf{E}) \overset{(S.13)}{\leq} \widetilde{\sigma},$$
$$

and with $ {MK} \lesssim {ML} \asymp J $ we have

$$
$$\|{\mathbb{E}\left\lbrack  {{\mathbf{E}}^{\top }{\mathbf{U}}^{ * }{\mathbf{U}}^{*\top }\mathbf{E}}\right\rbrack  }\| = \mathop{\max }\limits_{{l \in  \left\lbrack  L\right\rbrack  }}\|{\mathbb{E}\left\lbrack  {{\mathbf{E}}_{ : ,{S}_{l}}^{\top }{\mathbf{U}}^{ * }{\mathbf{U}}^{*\top }{\mathbf{E}}_{ : ,{S}_{l}}}\right\rbrack  }\| \leq  \mathop{\max }\limits_{{l \in  \left\lbrack  L\right\rbrack  }}\mathbb{E}\|{{\mathbf{E}}_{ : ,{S}_{l}}^{\top }{\mathbf{U}}^{ * }{\mathbf{U}}^{*\top }{\mathbf{E}}_{ : ,{S}_{l}}}\|$$
$$

$$
$$= M\mathop{\max }\limits_{{j \in  \left\lbrack  J\right\rbrack  }}\mathbb{E}\left\lbrack  {{\mathbf{E}}_{ : ,j}^{\top }{\mathbf{U}}^{ * }{\mathbf{U}}^{*\top }{\mathbf{E}}_{ : ,j}}\right\rbrack   \leq  M{\sigma }^{2}{\|{\mathbf{U}}^{ * }\|}_{F}^{2} = {MK}{\sigma }^{2},$$
$$

$$
$$\|{\mathbb{E}\left\lbrack  {{\mathbf{U}}^{*\top }\mathbf{E}{\mathbf{E}}^{\top }{\mathbf{U}}^{ * }}\right\rbrack  }\| \leq  \|{\mathbb{E}\left\lbrack  {\mathbf{E}{\mathbf{E}}^{\top }}\right\rbrack  }\| \leq  {\sigma }^{2}J,$$
$$

$$
$$\sigma \left( {{\mathbf{E}}^{\top }{\mathbf{U}}^{ * }}\right)  \leq  \sigma \sqrt{J} + \sigma \sqrt{MK},$$
$$

$$
$$R\left( {{\mathbf{E}}^{\top }{\mathbf{U}}^{ * }}\right)  = {\Bigg \|\mathop{\max }\limits_{{i \in  \left\lbrack  N\right\rbrack  ,l \in  \left\lbrack  L\right\rbrack  }}\|{\mathbf{E}}_{i,{S}_{l}}^{\top }{\mathbf{U}}_{i, : }^{ * }\|\Bigg \|}_{\infty } \leq  \sqrt{M}B{\|{\mathbf{U}}^{ * }\|}_{2,\infty },$$
$$

$$
$$v\left( {{\mathbf{E}}^{\top }{\mathbf{U}}^{ * }}\right)  \leq  \mathop{\max }\limits_{{l \in  \left\lbrack  L\right\rbrack  }}{\|\mathbb{E}\left\lbrack  {\mathbf{E}}_{ : ,{S}_{l}}^{\top }{\mathbf{U}}^{ * }{\mathbf{U}}^{*\top }{\mathbf{E}}_{ : ,{S}_{l}}\right\rbrack  \|}^{\frac{1}{2}} \leq  \sqrt{MK}\sigma ,$$
$$

$$
$${\sigma }_{ * }{\left( {\mathbf{U}}^{*\top }\mathbf{E}\right) }^{2} \leq  {\sigma }_{ * }{\left( \mathbf{E}\right) }^{2}\overset{\text{ by (S.13) }}{ \leq  }{\widetilde{\sigma }}^{2} \leq  M{\sigma }^{2}.$$
$$

43
