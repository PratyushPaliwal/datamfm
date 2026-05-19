40

## ROMAN SHVYDKOY

Since $ E > 4\bar{n} $ , we have $ \mathrm{x} + \mathrm{v} \geqslant E/4 $ , and hence, from the above,

$$
$$\left| I\right| E \lesssim  {\int }_{I}\left( {\mathrm{x} + \mathrm{v}}\right) \mathrm{d}t \lesssim  \mathop{\sum }\limits_{i}{\left| I\right| }^{{\delta }_{i}^{\prime }}{E}^{{\delta }_{i}^{\prime \prime }},$$
$$

which finishes the proof.

This finishes the proof of Theorem 5.1.

# # 6. APPENDIX: INTERPOLATION IN WEIGHTED SOBOLEV SPACES

For any any $ p \in \mathbb{N} $ we denote for short $ {\partial }_{x}^{p}f = \left( {{\partial }_{{x}_{1}}^{p}f,\ldots ,{\partial }_{{x}_{n}}^{p}f}\right) $ , and $ {\left| {\partial }_{x}^{p}f\right| }^{2} = \mathop{\sum }\nolimits_{i}{\left| {\partial }_{{x}_{i}}^{p}f\right| }^{2} $ . Similar notation will be used in $ v $ -variable. It is clear that $ {\left| {\partial }_{x}^{p}f\right| }^{2} $ represents a linear combination of $ p $th order derivatives.

Let us first note the following simple interpolation inequality: for $ k,l \geqslant 0 $ and $ K,L > 0 $ such that $ \frac{k}{K} + \frac{l}{L} < 1 $ and any $ \left| \mathbf{k}\right| = k,\left| \mathbf{l}\right| = l $, we have

$$
$${\int }_{\Omega  \times  {\mathbb{R}}^{n}}{\left| {\partial }_{x}^{\mathbf{k}}{\partial }_{v}^{\mathbf{l}}f\right| }^{2}\mathrm{\;d}v\mathrm{\;d}x \leqslant  {\left( {\int }_{\Omega  \times  {\mathbb{R}}^{n}}{\left| {\partial }_{x}^{K}f\right| }^{2}\mathrm{\;d}v\mathrm{\;d}x\right) }^{\frac{k}{K}}{\left( {\int }_{\Omega  \times  {\mathbb{R}}^{n}}{\left| {\partial }_{v}^{L}f\right| }^{2}\mathrm{\;d}v\mathrm{\;d}x\right) }^{\frac{l}{L}}{\left( {\int }_{\Omega  \times  {\mathbb{R}}^{n}}{\left| f\right| }^{2}\mathrm{\;d}v\mathrm{\;d}x\right) }^{1 - \frac{k}{K} - \frac{l}{L}}.\tag{131}$$
$$

Indeed, denoting by $ \mathrm{d}\xi $ the counting measure over $ {\mathbb{Z}}^{n} $ ,

$$
$$\int_{\Omega\times\mathbb{R}^{n}}|\partial_{x}^{\mathbf{k}}\partial_{v}^{\mathbf{l}}f|^{2}\mathrm{d}v\mathrm{d}x=\int_{\mathbb{Z}^{n}\times\mathbb{R}^{n}}\Pi_{i=1}^{n}|\xi_{i}|^{2k_{i}}|\eta_{i}|^{2l_{i}}|\hat{f}|^{2}\mathrm{d}\eta\mathrm{d}\xi\leqslant\int_{\mathbb{Z}^{n}\times\mathbb{R}^{n}}|\xi|^{2k}|\eta|^{2l}|\hat{f}|^{2}\mathrm{d}\eta\mathrm{d}\xi$$
$$

$$
$$\leqslant\int_{\mathbb{Z}^{n}\times\mathbb{R}^{n}}|\xi|^{2k}|\hat{f}|^{2k/K}|\eta|^{2l}|\hat{f}|^{2l/L}|\hat{f}|^{2(1-k/K-l/K)}\mathrm{d}\eta\mathrm{d}\xi$$
$$

$$
$$\leqslant\left(\int_{\mathbb{Z}^{n}\times\mathbb{R}^{n}}|\xi|^{2K}|\hat{f}|^{2}\mathrm{d}\eta\mathrm{d}\xi\right)^{\frac{k}{K}}\left(\int_{\mathbb{Z}^{n}\times\mathbb{R}^{n}}|\eta|^{2L}|\hat{f}|^{2}\mathrm{d}\eta\mathrm{d}\xi\right)^{\frac{1}{L}}\left(\int_{\mathbb{Z}^{n}\times\mathbb{R}^{n}}|f|^{2}\mathrm{d}\eta\mathrm{d}\xi\right)^{1-\frac{k}{K}-\frac{l}{L}}$$
$$

$$
$$\lesssim\left(\sum_{i}\int_{\mathbb{Z}^{n}\times\mathbb{R}^{n}}|\xi_{i}|^{2K}|\hat{f}|^{2}\mathrm{d}\eta\mathrm{d}\xi\right)^{\frac{k}{K}}\left(\sum_{i}\int_{\mathbb{Z}^{n}\times\mathbb{R}^{n}}|\eta_{i}|^{2L}|\hat{f}|^{2}\mathrm{d}\eta\mathrm{d}\xi\right)^{\frac{l}{L}}$$
$$

$$
$$\times\left(\int_{\mathbb{Z}^{n}\times\mathbb{R}^{n}}|f|^{2}\mathrm{d}\eta\mathrm{d}\xi\right)^{1-\frac{k}{K}-\frac{l}{L}}$$
$$

$$
$$=\left(\int_{\Omega\times\mathbb{R}^{n}}|\partial_{x}^{K}f|^{2}\mathrm{d}v\mathrm{d}x\right)^{\frac{k}{K}}\left(\int_{\Omega\times\mathbb{R}^{n}}|\partial_{v}^{L}f|^{2}\mathrm{d}v\mathrm{d}x\right)^{\frac{l}{L}}\left(\int_{\Omega\times\mathbb{R}^{n}}|f|^{2}\mathrm{d}v\mathrm{d}x\right)^{1-\frac{k}{K}-\frac{l}{L}}.$$
$$

When a weight is involved that depends only on $ v,\omega = \omega \left( v\right) $ , then the above interpolation extends trivially in the case when $ \mathbf{k} = 0 $ by application of (131) in $ x $-variable only, and the Hölder inequality in $ v $:

$$
$$\int_{\Omega\times\mathbb{R}^{n}}|\partial_{x}^{\mathbf{k}}f|^{2}\omega\mathrm{d}v\mathrm{d}x\leqslant\int_{\mathbb{R}^{n}}\left(\int_{\Omega}|\partial_{x}^{K}f|^{2}\mathrm{d}x\right)^{\frac{k}{K}}\left(\int_{\Omega}|f|^{2}\mathrm{d}x\right)^{1-\frac{k}{K}}\omega\mathrm{d}v\tag{132}$$
$$

$$
$$\leqslant\left(\int_{\Omega\times\mathbb{R}^{n}}|\partial_{x}^{K}f|^{2}\omega\mathrm{d}v\mathrm{d}x\right)^{\frac{k}{K}}\left(\int_{\Omega\times\mathbb{R}^{n}}|f|^{2}\omega\mathrm{d}v\mathrm{d}x\right)^{1-\frac{k}{K}}.$$
$$

It is clear that the above inequalities extend to any fractional $k$, $K$ as well if we replace the derivatives with Fourier multipliers $ {D}_{x}^{k}f $ with symbol $ {\left| \xi \right| }^{k} $. In fact the computations above already use that symbol even for integer order derivatives. It is important to keep in mind though that if $ k $ is integer,then since $ \omega $ is not involved in Fourier transform, we have

$$
$${\int }_{\Omega  \times  {\mathbb{R}}^{n}}{\left| {D}_{x}^{k}f\right| }^{2}\omega \mathrm{d}v\mathrm{\;d}x \sim  {\int }_{\Omega  \times  {\mathbb{R}}^{n}}{\left| {\partial }_{x}^{k}f\right| }^{2}\omega \mathrm{d}v\mathrm{\;d}x.$$
$$

In other words we can go back to the classical derivatives.

Lemma 6.1. *Suppose $ \omega $ is a doubling weight,*

$$
$$c \leqslant\frac{\omega \left( {v}^{\prime }\right) }{\omega \left( {v}^{\prime \prime }\right) } \leqslant C,\;\frac{1}{2} \leqslant  \frac{\left| {v}^{\prime }\right| }{\left| {v}^{\prime \prime }\right| } \leqslant  2\tag{133}$$
$$

$$
$$\omega(v)\sim1,\quad|v|\leqslant1.$$
$$
