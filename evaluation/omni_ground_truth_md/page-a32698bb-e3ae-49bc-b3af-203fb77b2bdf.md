36

## CHOI, JUNG, AND LEE

# #### Appendix C. Proof of Lemma 3.3

Here, we provide detailed proof for Lemma 3.3. We only establish (3.17) since the other estimate can be derived through a similar argument. We write $ B = {B}_{\mathfrak{M}} $ for simplicity. By using the Littlewood-Paley theorem, we get

By using the Littlewood-Paley theorem, we get

$$
$${\| \langle \nabla {\rangle }^{{\alpha }_{1}}{D}^{{\alpha }_{2}}B\left\lbrack  f,g\right\rbrack  \| }_{{L}^{{l}_{1}^{\prime }}}^{2} \lesssim  {\| {P}_{ \leq  1}B\left\lbrack  f,g\right\rbrack  \| }_{{L}^{{l}_{1}^{\prime }}}^{2} + \mathop{\sum }\limits_{{N > 1}}{N}^{2\left( {{\alpha }_{1} + {\alpha }_{2}}\right) }{\| {P}_{N}B\left\lbrack  f,g\right\rbrack  \| }_{{L}^{{l}_{1}^{\prime }}}^{2}, \tag{C.1}$$
$$

where $ {D}^{{\alpha }_{2}} = \left\langle {\left| \nabla \right| }^{{\alpha }_{2}}\right\rangle $ or $ {D}^{{\alpha }_{2}} = {\left| \nabla \right| }^{{\alpha }_{2}} $ . The first term can be estimated as follows:

$$
$${\| {P}_{ \leq  1}B\left\lbrack  f,g\right\rbrack  \| }_{{L}^{{l}_{1}^{\prime }}} \lesssim  \parallel f{\parallel }_{{L}^{{l}_{2}}}\parallel g{\parallel }_{{L}^{2}}.$$
$$

For the second term, we observe

$$
$$\| {P}_{N}B\left\lbrack  f,g\right\rbrack  \| _{{L}^{{l}_{1}^{\prime }}} \lesssim  \| {P}_{N}B\left\lbrack  {P}_{ \leq  \frac{N}{8}}f,g\right\rbrack  \| _{{L}^{{l}_{1}^{\prime }}} + \mathop{\sum }\limits_{{M > \frac{N}{8}}}\| {P}_{N}B\left\lbrack  {P}_{M}f,g\right\rbrack  \| _{{L}^{{l}_{1}^{\prime }}}.$$
$$

By using (3.16), we deduce

$$
$$\| {P}_{N}B\left\lbrack  {P}_{ \leq  \frac{N}{8}}f,g\right\rbrack  \| _{{L}^{{l}_{1}^{\prime }}} \lesssim  \| B\left\lbrack  {P}_{ \leq  \frac{N}{8}}f,{P}_{\frac{N}{8} < \cdot < {8N}}g\right\rbrack  \| _{{L}^{{l}_{1}^{\prime }}} \lesssim  \| {P}_{ \leq  \frac{N}{8}}f\| _{{L}^{{l}_{2}}}\| {P}_{\frac{N}{8} < \cdot < {8N}}g\| _{{L}^{2}} \lesssim  \parallel f{\parallel }_{{L}^{{l}_{2}}}\mathop{\sum }\limits_{{M \sim  N}}\| {P}_{M}g\| _{{L}^{2}}.$$
$$

Consequently, we arrive at

$$
$$\mathop{\sum }\limits_{{N > 1}}{N}^{2\left( {{\alpha }_{1} + {\alpha }_{2}}\right) }\| {P}_{N}B\left\lbrack  {P}_{ \leq  \frac{N}{8}}f,g\right\rbrack  \| ^2_{{L}^{{l}_{1}^{\prime }}} \lesssim  \| f\|_{{L}^{{l}_{2}}}^{2}\mathop{\sum }\limits_{{N > 1}}\left(\mathop{\sum }\limits_{{M \sim  N}}{N}^{{\alpha }_{1} + {\alpha }_{2}}\| {P}_{Mg}\| _{{L}^{2}}\right)^{2}$$
$$

$$
$$\lesssim\|f\|_{L^{l_{2}}}^{2}\sum_{M\gtrsim1}M^{2(\alpha_{1}+\alpha_{2})}\|P_{M}g\|_{L^{2}}^{2}$$
$$

$$
$$\lesssim\|f\|_{L^{l_{2}}}^{2}\|g\|_{\dot{H}^{\alpha_{1}+\alpha_{2}}}^{2}.$$
$$

Meanwhile, we find

$$
$$\mathop{\sum }\limits_{{M > \frac{N}{8}}}{\| {P}_{N}B\left\lbrack  {P}_{M}f,g\right\rbrack  \| }_{{L}^{{l}_{1}^{\prime }}} \lesssim  \mathop{\sum }\limits_{{M > \frac{N}{8}}}{\| {P}_{M}f\| }_{{L}^{2}}\parallel g{\parallel }_{{L}^{{l}_{2}}} \lesssim  \mathop{\sum }\limits_{{M > \frac{N}{8}}}\frac{1}{{M}^{{\alpha }_{1} + {\alpha }_{2}}}{\| {P}_{M}f\| }_{{\dot{H}}^{{\alpha }_{1} + {\alpha }_{2}}}\parallel g{\parallel }_{{L}^{{l}_{2}}}$$
$$

due to (3.16). Then, it follows that

$$
$$\sum_{N>1}N^{2(\alpha_1+\alpha_2)}\left(\sum_{M>\frac{N}{8}}\|P_NB[P_Mf,g]\|_{L^{l_1^{\prime}}}\right)^2$$
$$

$$
$$\lesssim\sum_{N>1}\left(\sum_{M>\frac{N}{8}}\left(\frac{N}{M}\right)^{\alpha_{1}+\alpha_{2}}\|P_{M}f\|_{\dot{H}^{\alpha_{1}+\alpha_{2}}}\|g\|_{L^{l_{2}}}\right)^{2}$$
$$

$$
$$\lesssim\|g\|_{L^{l_{2}}}^{2}\sum_{N>1}\left(\sum_{M>\frac{N}{8}}\left(\frac{N}{M}\right)^{\alpha_{1}+\alpha_{2}}\sum_{M>\frac{N}{8}}\left(\frac{N}{M}\right)^{\alpha_{1}+\alpha_{2}}\|P_{M}f\|_{\dot{H}^{\alpha_{1}+\alpha_{2}}}^{2}\right)$$
$$

$$
$$\lesssim  \parallel g{\parallel }_{{L}^{{l}_{2}}}^{2}\mathop{\sum }\limits_{{M> {\frac{1}{8}}}} {\mathop{\sum }\limits_{{1<N<8M}}{\left( \frac{N}{M}\right) }^{{\alpha }_{1} + {\alpha }_{2}}\ ~\| {P}_{M}f\|^{2} _{{\dot{H}}^{\alpha_{1} + \alpha _2}}}$$
$$

$$
$$\lesssim\|g\|_{L^{l_{2}}}^2\sum_{M>\frac{1}{8}}\|P_{M}f\|_{\dot{H}^{\alpha_{1}+\alpha_{2}}}^2$$
$$

by the Cauchy-Schwartz inequality and the fact that

$$
$$\mathop{\sum }\limits_{{N < {8M}}}{\left( \frac{N}{M}\right) }^{{\alpha }_{1} + {\alpha }_{2}} \lesssim  1.$$
$$
