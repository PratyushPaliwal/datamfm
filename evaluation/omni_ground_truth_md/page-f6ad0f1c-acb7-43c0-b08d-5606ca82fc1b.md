## FOKKER-PLANCK-ALIGNMENT EQUATIONS

19

We now test (80) against $ {G}^{\prime }\left( \frac{{\left( \theta f\right) }_{{\varepsilon }_{1}}}{\theta + {\varepsilon }_{2}}\right) $, and integrate in time:

$$
$${ \int _ { \Omega \times \mathbb { R } ^ { n } \times \{ t\} } } G \left( \frac { ( \theta f ) _ { \varepsilon _ { 1 } } } { \theta + \varepsilon _ { 2 } } \right) \varphi \mathrm { d } v \mathrm { d } x - \int _ { \Omega \times \mathbb { R } ^ { n } \times \{ 0 \} } G \left( \frac { ( \theta f ) _ { \varepsilon _ { 1 } } } { \theta + \varepsilon _ { 2 } } \right) \varphi \mathrm { d } v \mathrm { d } x - \int _ { 0 } ^ { t } \int _ { \Omega \times \mathbb { R } ^ { n } \times \{ t \} } G \left( \frac { ( \theta f ) _ { \varepsilon _ { 1 } } } { \theta + \varepsilon_ { 2 } } \right) \partial _t \varphi \mathrm { d }v\mathrm { d } x \mathrm { d } s$$
$$

$$
$$={ - \int _ { 0 } ^ { t } \int _ { \Omega \times \mathbb { R } ^ { n } } \frac { ( \theta v \cdot \nabla _ { x } f ) _ { \varepsilon _ { 1 } } } { \theta + \varepsilon _ { 2 } } G ^ { \prime } \left( \frac { ( \theta f ) _ { \varepsilon _ { 1 } } } { \theta + \varepsilon _ { 2 } } \right) \varphi \mathrm { d } v \mathrm { d } x \mathrm { d } s + \int _ { 0 } ^ { t } \int _ { \Omega \times \mathbb { R } ^ { n } } \frac { ( \theta _ { S_\rho} \Delta_v f  ) _ { \varepsilon _ { 1 } } } { \theta + \varepsilon _ { 2 } } G ^ { \prime } \left( \frac { ( \theta f ) _ { \varepsilon _ { 1 } } } { \theta + \varepsilon _ { 2 } } \right) \varphi \mathrm { d } v \mathrm { d } x \mathrm { d } s }$$
$$

$$
$$+ {\int }_{0}^{t}{\int }_{\Omega  \times  {\mathbb{R}}^{n}}\frac{{\nabla }_{v} \cdot  {\left( \theta {\mathrm{s}}_{\rho }vf\right) }_{{\varepsilon }_{1}}}{\theta  + {\varepsilon }_{2}}{G}^{\prime }\left( \frac{{\left( \theta f\right) }_{{\varepsilon }_{1}}}{\theta  + {\varepsilon }_{2}}\right) \varphi \mathrm{d}v\mathrm{\;d}x\mathrm{\;d}s - {\int }_{0}^{t}{\int }_{\Omega  \times  {\mathbb{R}}^{n}}\frac{{\nabla }_{v} \cdot  {\left( \theta {\mathrm{w}}_{\rho }f\right) }_{{\varepsilon }_{1}}}{\theta  + {\varepsilon }_{2}}{G}^{\prime }\left( \frac{{\left( \theta f\right) }_{{\varepsilon }_{1}}}{\theta  + {\varepsilon }_{2}}\right) \varphi \mathrm{d}v\mathrm{\;d}x\mathrm{\;d}s$$
$$

$$
$$+ \int _ { 0 } ^ { t } \int _ { \Omega \times \mathbb { R } ^ { n } } \left[ \frac { ( f \partial _ { t } \theta ) _ { \varepsilon _ { 1 } } } { \theta + \varepsilon _ { 2 } } - \frac { ( \theta f ) _ { \varepsilon _ { 1 } } \partial _ { t } \theta } { \left[ \theta + \varepsilon _ { 2 } \right]^2 } \right]{G}^{\prime }\left( \frac{{\left( \theta f\right) }_{{\varepsilon }_{1}}}{\theta + {\varepsilon }_{2}}\right) \varphi \mathrm { d } v \mathrm { d }x \mathrm { d } s := - I + I I + I I I - I V +V.$$
$$

Let us note that $ \theta $ satisfies the mollified continuity equation

$$
$${\partial }_{t}\theta  =  - \left( {u\rho }\right)  * \nabla {\chi }_{{r}_{0}},$$
$$

and so,

$$
$$\|{\partial}_{t}\theta \|_{\infty } \lesssim \parallel u{\parallel }_{{L}_{\rho }^{2}} \lesssim C.\tag{81}$$
$$

In what follows we will be taking consecutive limits as $ {\varepsilon }_{1} \rightarrow 0 $and then $ {\varepsilon }_{2} \rightarrow 0 $.

The left hand side converges to its natural limit since $ G $ is smooth and $ \frac{{\left( \theta f\right) }_{{\varepsilon }_{1}}}{\theta + {\varepsilon }_{2}} \rightarrow \frac{\theta f}{\theta + {\varepsilon }_{2}} \rightarrow f $pointwise almost everywhere. So, we obtain

$$
$${\int }_{\Omega  \times  {\mathbb{R}}^{n}\times \{ t\} }G\left( f\right) \varphi \mathrm{d}v\mathrm{\;d}x - {\int }_{\Omega  \times  {\mathbb{R}}^{n}\times \{ 0\} }G\left( f\right) \varphi \mathrm{d}v\mathrm{\;d}x - {\int }_{0}^{t}{\int }_{\Omega  \times  {\mathbb{R}}^{n}\times \{ t\} }G\left( f\right) {\partial }_{t}\varphi \mathrm{d}v\mathrm{\;d}x\mathrm{\;d}s.$$
$$

*LIMIT OF $ I $*. Let us go back to $ I $. Integrating by parts we have

$$
$${I= - \int _ { 0 } ^ { t } \int _ { \Omega \times \mathbb { R } ^ { n } } \frac { \bigl ( f v \cdot \nabla \theta \bigr ) _ { \varepsilon _ { 1 } } } { \theta + \varepsilon _ { 2 } } G ^ { \prime } ( \frac { ( \theta f ) _ { \varepsilon _ { 1 } } } { \theta + \varepsilon _ { 2 } } ) \varphi~ \mathrm { d } v ~\mathrm { d } x ~\mathrm { d } s }$$
$$

$$
$$+ \int _ { 0 } ^ { t } \int _ { \Omega \times \mathbb { R } ^ { n } } \frac { \bigl ( f v \theta \bigr ) \ast \nabla _ { x } \chi _ { \varepsilon _ { 1 } } } { \theta + \varepsilon _ { 2 } } G ^ { \prime } ( \frac { ( \theta f ) _ { \varepsilon _ { 1 } } } { \theta + \varepsilon _ { 2 } } ) \varphi \mathrm { d } v \mathrm { d } x \mathrm { d } s :=I_1+I_2 .$$
$$

For the limit of $ {I}_{1} $, we have $ {fv} \cdot \nabla \theta \in {L}^{1} $, so, $ {\left( fv \cdot \nabla \theta \right) }_{{\varepsilon }_{1}} \rightarrow {fv} \cdot \nabla \theta $ in $ {L}^{1} $, while$ {G}^{\prime }\left( \frac{{\left( \theta f\right) }_{{\varepsilon }_{1}}}{\theta + {\varepsilon }_{2}}\right) \rightarrow {G}^{\prime }\left( \frac{\theta f}{\theta + {\varepsilon }_{2}}\right) $ a.e. and is uniformly bounded. Consequently, by dominated convergence,

$$
$${I}_{1} \rightarrow   - {\int }_{0}^{t}{\int }_{\Omega  \times  {\mathbb{R}}^{n}}\frac{{fv} \cdot  \nabla \theta }{\theta  + {\varepsilon }_{2}}{G}^{\prime }\left( \frac{\theta f}{\theta  + {\varepsilon }_{2}}\right) \varphi~\mathrm{d}v\mathrm{\;d}x\mathrm{\;d}s.\tag{82}$$
$$

We will leave it at that for now, and turn to $ {I}_{2} $. Observe

$$
$$( f v \theta ) * \nabla _ { x } \chi _ { \varepsilon _ { 1 } } =  \int _ { \Omega \times \mathbb R ^ { n } } f ( y , w ) w \theta ( y ) \nabla _ { x } \chi _ { \varepsilon _ { 1 } } ( x - y , v - w ) { \mathrm { d } } w~{ \mathrm { d } } y$$
$$

$$
$$\qquad = \int _ { \Omega \times \mathbb R ^ { n } } f ( y , w ) ( w - v ) \theta ( y ) \nabla _ { x } \chi _ { \varepsilon _ { 1 } } ( x - y , v - w ) { \mathrm { d } } w~{ \mathrm { d } } y + v \cdot \nabla _ { x } ( f \theta ) _ { \varepsilon _ { 1 } }$$
$$

using that $ w{\nabla }_{x}{\chi }_{{\varepsilon }_{1}}\left( {\cdot ,w}\right) $ is odd in $ w $, we can insert $ f\left( {y,v}\right) $,

$$
$$(fv \theta ) * \nabla _ { x } \chi _ { \varepsilon _ { 1 } } =  \int _ { \Omega \times \mathbb R ^ { n } } \bigl [ f ( y , w ) - f ( y , v ) \bigr ] ( w - v ) \theta ( y ) \nabla _ { x } \chi _ { \varepsilon _ { 1 } } ( x - y , v - w ) \mathrm { d } w \mathrm { d } y + v \cdot \nabla _ { x } \bigl ( f \theta \bigr ) _ { \varepsilon _ { 1 } }\tag{83}$$
$$

$$
$$=  \int _ { 0 } ^ { 1 } \int _ { \Omega \times \mathbb R ^ { n } } \theta ( x - y ) \nabla _ { v } f ( x - y , v + \theta w ) w \otimes w \nabla _ { x } \chi _ { \varepsilon _ { 1 } } ( y , w ) \mathrm { d } w \mathrm { d } y \mathrm { d } \theta + v \cdot \nabla _ { x } \bigl ( \theta f )_ { \varepsilon _ { 1 } }.$$
$$
