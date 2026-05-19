For $ {\beta }_{1}^{\prime } $, with (S.17) we have with probability at least $ 1 - O( {n}^{-{10}}) $

$$
$$\beta _ { 1 } ^ { \prime } = \left\| { \mathbf { R } ^ { * } } ^ { \top } \left( { \mathbf { U U } ^ { \top } } { \mathbf { U } ^ { * } } - { \mathbf { U } ^ { * } } \right) \right\| _ { 2 , \infty }$$
$$

$$
$$\leq  {\sigma }_{1}^{ * }{\|{\mathbf{V}}^{ * }\|}_{2,\infty }\left\|{{\mathbf{U}}^{*\top }\mathbf{U}{\mathbf{U}}^{\top }{\mathbf{U}}^{ * } - {\mathbf{I}}_{K}}\right\| \lesssim  \frac{{\kappa }^{ * }{\sigma }^{2}\left( {{MN} + J}\right) }{{\sigma }_{K}^{ * }}{\|{\mathbf{V}}^{ * }\|}_{2,\infty }. \tag{S.33}$$
$$

For $ {\beta }_{2}^{\prime } $, introducing the "leave-one-block-out" alternative$ {\mathbf{U}}^{( j) } $yields that

$$
$${ \beta } _ { 2 } ^ { \prime } = \mathop{\max }\limits_ { j \in [ J ] } \left|\left| \mathbf { E } _ { : , j } ^ { \top } \left( \mathbf { U U } ^ { \top } \mathbf { U } ^ { * } - \mathbf { U } ^ { * } \right) \right|\right| _ { 2 }$$
$$

$$
$$\leq  \underset{{\gamma }_{1}^{\prime }}{\underbrace{\mathop{\max }\limits_{{j \in  \left\lbrack  J\right\rbrack  }}\left\|{{\mathbf{E}}_{ : ,j}^{\top }\left( {{\mathbf{U}}^{( j) }{\mathbf{U}}^{( j) ^{\top }}{\mathbf{U}}^{ * } - {\mathbf{U}}^{ * }}\right) }\right\|}} + \underset{{\gamma }_{2}^{\prime }}{\underbrace{\mathop{\max }\limits_{{j \in  [J] }}\left\|{{\mathbf{E}}_{ : ,j}^{\top }\left( {\mathbf{U}{\mathbf{U}}^{\top }{\mathbf{U}}^{ * } - {\mathbf{U}}^{( j) }{\mathbf{U}}^{{( j)}^{\top }}{\mathbf{U}}^{ * }}\right) }\right\|}} .\tag{S.34}$$
$$

Upper bounding $ {\gamma }_{1}^{\prime } $ in (S.34). Utilizing Lemma S.4, one has at least $ 1 - O\left( {d}^{-{11}}\right) $ that,

$$
$$\gamma _{1}^{\prime} \leq \sigma \sqrt { \log d } \underset { j \in [ J ] } { \max } \| \mathbf { U } ^ { (j) } \mathbf { U } ^ { (j) ^ { \top } } \mathbf { U } ^ { * } - \mathbf { U } ^ { * }  \|_ { F } + B \log d \underset { j \in [ J ] } { \max } \| \mathbf { U } ^ { (j) } \mathbf { U } ^ { (j) ^ { \top } } \mathbf { U } ^ { * } - \mathbf { U } ^ { * } \| _ { 2 , \infty }$$
$$

$$
$$\leq  \sigma \sqrt{\log d}{\|{\mathbf{{UU}}}^{\top }{\mathbf{U}}^{ * } - {\mathbf{U}}^{ * }\|}_{F} + \sigma \sqrt{\log d}\mathop{\max }\limits_{j \in  [J]}{\|{\mathbf{U}}^{\left( j\right) }{\mathbf{U}}^{\left( j\right) \top }{\mathbf{U}}^{ * } - \mathbf{U}{\mathbf{U}}^{\top }{\mathbf{U}}^{ * }\|}_{F}$$
$$

$$
$$+ B \log d \| \mathbf { U } \mathbf { U } ^ { \top } \mathbf { U } ^ { * } - \mathbf { U } ^ { * } \| _ {2, \infty } + B \log d\mathop{\max }\limits_{j \in  [J]}  \| \mathbf { U } ^ { (j) } \mathbf { U } ^ { (j)^\top }\mathbf { U } ^ { * }  - \mathbf { U } \mathbf { U } ^ { \top } \mathbf { U } ^ { * } \| _ { 2 , \infty }$$
$$

$$
$$\leq \sigma \sqrt { \log d}~ \| \mathbf { U } \mathbf { U } ^ { \top } \mathbf { U } ^ { * } - \mathbf { U } ^ { * } \| _ { F } + B \log d \| \mathbf { U } \mathbf { U } ^ { \top } \mathbf { U } ^ { * } - \mathbf { U } ^ { * } \| _ { 2 , \infty }$$
$$

$$
$$+ ( \sigma \sqrt { \log d } + B \log d ) \mathop{\max }\limits_{j \in  [J]} \Big \|\mathbf { U }^{(j)} \mathbf { U }^{(j)^{\top}} -\mathbf { U } \mathbf { U } ^ { \top} \Big \| _ { F }$$
$$

$$
$$\lesssim \sigma \sqrt { \log d }~ \| \mathbf { U } \mathbf { U } ^ { \top } \mathbf { U } ^ { * } - \mathbf { U } ^ { * } \| _ { F } + B \log d \| \mathbf { U } \mathbf { U } ^ { \top } \mathbf { U }^ { * } -\mathbf { U }^ { * }\| _{2 , \infty}$$
$$

$$
$$+ B \log d ~\| \mathbf { U }^{(j)} \mathbf { U } ^ {(j)^ \top } -\mathbf { U }\mathbf { U } ^  \top\| _F,\tag{S.35}$$
$$

where the last line holds since $ \sigma \sqrt{\log d} \ll B\log d $ .

To bound $\max_{j \in [J]} \| {\mathbf{U}}^{( j) }{\mathbf{U}}^{(j) ^{\top }} - \mathbf{U}{\mathbf{U}}^{\top }\| _{F} $in the RHS above, we apply Wedin’s theorem with (S.31) and obtain

$$
$$\max \left\{ \left\| \mathbf { U U } ^ { \top } - \mathbf { U } ^ { ( j ) } \mathbf { U } ^ { ( j ) ^ { \top } } \right\| _ { F } , \left\| \mathbf { V } \mathbf { V } ^ { \top } - \mathbf { V } ^ { ( j ) } \mathbf { V } ^ { ( j ) ^ { \top } } \right\| _ { F } \right\}$$
$$

$$
$$\lesssim \frac { \max\left\{ \left\| \mathcal { P } _ { : , S _ { l _ { j } } } ( \mathbf { E } ) ^ { \top } \mathbf { U } ^ { ( j ) } \right\| _ { F } , \left\| \mathcal { P } _ { : , S _ { l _ { j } } } ( \mathbf { E } ) \mathbf { V } ^ { ( j ) } \right\| _ { F } \right\} } { \sigma _ { K } ^ { * } } .\tag{S.36}$$
$$

51
