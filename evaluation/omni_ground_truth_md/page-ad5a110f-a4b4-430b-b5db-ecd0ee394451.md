## KOLMOGOROV EQUATIONS FOR 2D SCBF EQUATIONS

29

$$
$$\le C \lambda _ { 1 } ^ { \delta ( 2 - 8 \delta ) }  \int _ { \{ \| { \pmb x } \| _ { \mathbb { V } } \geq \varepsilon ^ { - 1 } \} } e ^ { \kappa \| { \pmb x } \| _ { \mathbb { H } } ^ { 2 } } \| \mathrm { A } ^ { \delta } { \pmb x } \| _ { \mathbb { H } } ^ { 8 \delta } \frac { \| \mathrm { A } ^ { \delta + \frac { 1 } { 2 } } { \pmb x } \| _ { \mathbb { H } } ^ { 2 } } { \| { \pmb x } \| _ { \mathbb { V } } ^ { 8 \delta - 2 } } \eta ( \mathrm { d } { \pmb x } )$$
$$

$$
$$\le C \lambda _ { 1 } ^ { \delta ( 2 - 8 \delta ) } \varepsilon ^ { 8 \delta - 2 }  \int _ { \mathbb { H } } e ^ { \kappa \| { \pmb x } \| _ { \mathbb { H } } ^ { 2 } } \| \mathrm { A } ^ { \delta } { \pmb x } \| _ { \mathbb { H } } ^ { 8 \delta } \| \mathrm { A } ^ { \delta + \frac { 1 } { 2 } } { \pmb x } \| _ { \mathbb { H } } ^ { 2 } \eta ( \mathrm { d } { \pmb x } )$$
$$

$$
$$\le C \varepsilon ^ { 8 \delta - 2 } , \tag{6.18}$$
$$

provided $ \frac{1}{4} < \delta < \frac{1}{2} $, and thus (6.16) follows by an application of the Dominated convergence theorem. Let us now calculate by using (5.3) and (6.12)

$$
$$\int _ { \mathbb { H } } | ( \mathcal{C} _ { \varepsilon } ( x ) - \mathcal{C} ( x ) , \mathrm { D } _ { x } \varphi _ { \varepsilon } ( x ) ) | ^ { 2 } \eta ( \mathrm { d } x )$$
$$

$$
$$= \int _ { \{ \| x \|  _\mathbb{V} \geq \varepsilon ^ { - 1 } \} } | ( \mathcal{C} _ { \varepsilon } ( x ) - \mathcal{C} ( x ) , \mathrm { D } _ { x } \varphi _ { \varepsilon } ( x ) ) | ^ { 2 } \eta ( \mathrm { d } x )$$
$$

$$
$$\leq \int _ { \{ \| x \| _ { \mathbb{V} \geq \varepsilon ^ { - 1 } } \} } \left| \frac { 1 - \varepsilon ^ { r + 1 } \| x \| _ { \mathbb{V} } ^ { r + 1 } } { \varepsilon ^ { r + 1 } \| x \| _ { \mathbb{V} } ^ { r + 1 } } \right| \| \mathcal{C} ( x ) \| _ { \mathbb { H } } ^ { 2 } \| \mathrm { D } _ { x } \varphi _ { \varepsilon } ( x ) \| _ { \mathbb { H } } ^ { 2 } \eta ( \mathrm { d } x )$$
$$

$$
$$\leq C e ^ { - \delta t } \| f \| _ { 1 } ^ { 2 } \int _ { \{ \| x \| _ {\mathbb{V} \geq \varepsilon ^ { - 1 } } \} } e ^ { \kappa \| x \| _ { \mathbb { H } } ^ { 2 } } \| \mathcal{C}( x ) \| _ { \mathbb { H } } ^ { 2 } \eta ( \mathrm { d } x ) ,$$
$$

so that (6.15) follows if

$$
$$\mathop{\lim }\limits_{{\varepsilon  \rightarrow  0}}{\int }_{\left\{  \parallel \pmb x{\parallel }_{\mathbb{V}} \geq  {\varepsilon }^{-1}\right\}  }{e}^{\kappa \parallel \pmb x{\parallel }_{\mathbb{H}}^{2}}\parallel \mathcal{C}\left( \pmb x\right) {\parallel }_{\mathbb{H}}^{2}\eta \left( {\mathrm{d}\pmb x}\right)  = 0. \tag{6.19}$$
$$

We calculate for $ r = 2 $ by using (5.4), Ladyzhenskaya’s and Poincaré’s inequlaities

$$
$$\parallel \mathcal{C}\left( \pmb x\right) {\parallel }_{\mathbb{H}} \leq  \parallel\pmb x{\parallel }_{\widetilde{\mathbb{L}}^{4}}^{2} \leq  \sqrt{2}\parallel \pmb x{\parallel }_{\mathbb{H}}\parallel \mathbf{x}{\parallel }_{\mathbb{V}} \leq  \frac{\sqrt{2}}{{\lambda }_{1}}\parallel \pmb x{\parallel }_{\mathbb{V}}^{2} \leq  \frac{\sqrt{2}}{{\lambda }_{1}}{\|{\mathrm{\;A}}^{\delta }\pmb x\|}_{\mathbb{H}}^{4\delta }{\|{\mathrm{A}}^{\delta  + \frac{1}{2}}\pmb x\|}_{\mathbb{H}}^{2\left( {1 - {2\delta }}\right) }.$$
$$

Then proceeding in a similar way as we did in (6.17), one can conclude (6.19) provided $ \frac{1}{4} < \delta < \frac{1}{2} $ . Along with Lemma 5.1, (5.35), (6.18) and (2.5), it follows for $ r = 3 $ that

$$
$$\int_{\{\|\pmb x\|_\mathbb{V} \geq \varepsilon^{-1}\}} e^{\kappa \|\pmb x\|_H^2} \|\mathcal{C}(\pmb x)\|_H^2 \eta(d\pmb x)$$
$$

$$
$$\leq C \int_{\{\|\pmb x\|_\mathbb{V} \geq \varepsilon^{-1}\}} e^{\kappa \|\pmb x\|_\mathbb{H}^2} \|\pmb x\|_\mathbb{V}^4 \|\pmb x\|_\mathbb{H}^2 \eta(d\pmb x)$$
$$

$$
$$\leq  \frac{C}{{\lambda }_{1}^{2\delta }}{\int }_{\left\{  \parallel \pmb x {\parallel }_{\mathbb{V}} \geq  {\varepsilon }^{-1}\right\}  }{e}^{\kappa \parallel \pmb x {\parallel }_{\mathbb{H}}^{2}}{\|{\mathrm{A}}^{\delta } \pmb x \|}_{\mathbb{H}}^{8\delta }{\|{\mathrm{A}}^{\delta  + \frac{1}{2}}\pmb x \|}_{\mathbb{H}}^{4 - {8\delta }}{\|{\mathrm{A}}^{\delta }\pmb x \|}_{\mathbb{H}}^{2}\eta \left( {\mathrm{d}\pmb x }\right)$$
$$

$$
$$\leq \frac{C}{\lambda_1^{2\delta}} \int_{\{\|\pmb x\|_\mathbb{V} \geq \varepsilon^{-1}\}} e^{\kappa \|\pmb x\|_\mathbb{H}^2} \|A^{\delta} \pmb x\|_{\mathbb{H}}^{8\delta + 2}  \frac{\|A^{\delta + \frac{1}{2}} \pmb x\|_{\mathbb{H}}^2}{\|A^{\delta + \frac{1}{2}} \pmb x\|_{\mathbb{H}}^{8\delta - 2}}  \eta(d\pmb x)$$
$$

$$
$$\le C \lambda _ { 1 } ^ { \delta ( 2 - 8 \delta ) }  \int _ { \{ \| { \pmb x } \| _ { \mathbb { V } } \geq \varepsilon ^ { - 1 } \} } e ^ { \kappa \| { \pmb x } \| _ { \mathbb { H } } ^ { 2 } } \| \mathrm { A } ^ { \delta } { \pmb x } \| _ { \mathbb { H } } ^ { 8 \delta+2} \frac { \| \mathrm { A } ^ { \delta + \frac { 1 } { 2 } } { \pmb x } \| _ { \mathbb { H } } ^ { 2 } } { \| { \pmb x } \| _ { \mathbb { V } } ^ { 8 \delta - 2 } } \eta ( \mathrm { d } { \pmb x } )$$
$$

$$
$$\le C \lambda _ { 1 } ^ { \delta ( 2 - 8 \delta ) } \varepsilon ^ { 8 \delta - 2 }  \int _ { \mathbb { H } } e ^ { \kappa \| { \pmb x } \| _ { \mathbb { H } } ^ { 2 } } \| \mathrm { A } ^ { \delta } { \pmb x } \| _ { \mathbb { H } } ^ { 8 \delta+2 } \| \mathrm { A } ^ { \delta + \frac { 1 } { 2 } } { \pmb x } \| _ { \mathbb { H } } ^ { 2 } \eta ( \mathrm { d } { \pmb x } )$$
$$

$$
$$\le C \varepsilon ^ { 8 \delta - 2 } ,$$
$$
