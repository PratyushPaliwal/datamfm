Upper bounding $ {\gamma }_{2} $ in (S.21). Using (S.9) in Lemma S.5 and (S.28), we have with probability at least $ 1 - O\left( {d}^{-{10}}\right) $ that

$$
$$\gamma_{2}=\max_{i\in[N]}\left\|\mathbf{E}_{i,:}\left(\mathbf{V}\mathbf{V}^{\top}\mathbf{V}^{\ast}-\mathbf{V}^{(-i)}\mathbf{V}^{(-i)^\top}\mathbf{V}^{\ast}\right)\right\|$$
$$

$$
$$\lesssim\max_{i\in[N]}\|\mathbf{E}_{i,:}\|\left\|\mathbf{V}\mathbf{V}^{\top}-\mathbf{V}^{(-i)}\mathbf{V}^{(-i)^\top}\right\|$$
$$

$$
$$\lesssim\sigma\sqrt{J}\max_{i\in[N]}\left\|\mathbf{V}\mathbf{V}^{\top}-\mathbf{V}^{(-i)}\mathbf{V}^{(-i)^\top}\right\|$$
$$

$$
$$\lesssim\frac{\sigma\sqrt{J}}{\sigma_{K}^{*}}\left(\widetilde{\sigma}\sqrt{K\log d}+MB\log d\left\|\mathbf{V}^{*}\right\|_{2,\infty}+\sigma\sqrt{J}\left\|\mathbf{U}^{*}\right\|_{2,\infty}+\right.$$
$$

$$
$$\sigma\sqrt{J}\left\|\mathbf{U}\mathbf{U}^{\top}\mathbf{U}^{*}-\mathbf{U}^{*}\right\|_{2,\infty}+\gamma_{1}\Big).$$
$$

Combining (S.16) with the upper bounds for $ {\gamma }_{1} $ and $ {\gamma }_{2} $ , with $ \sigma \sqrt{J} = o\left( {\sigma }_{K}^{ * }\right) $ , we have with probability at least $ 1 - O\left( {d}^{-{10}}\right) $ that

$$
$$\beta_{2}\lesssim\frac{\widetilde{\sigma}\sigma\sqrt{K\left(MN+J\right)\log d}}{\sigma_{K}^{*}}+MB\log d\left\|\mathbf{V}\mathbf{V}^{\top}\mathbf{V}^{*}-\mathbf{V}^{*}\right\|_{2,\infty}$$
$$

$$
$$+{\frac{MB\log d}{\sigma_{K}^{*}}}\left(\widetilde{\sigma}\sqrt{K\log d}+MB\log d\left\|\mathbf{V}^{*}\right\|_{2,\infty}+\sigma\sqrt{J}\left\|\mathbf{U}^{*}\right\|_{2,\infty}\right.$$
$$

$$
$$+\sigma\sqrt{J}\left\|\mathbf{U}\mathbf{U}^{\top}\mathbf{U}^{*}-\mathbf{U}^{*}\right\|_{2,\infty}\Big)$$
$$

$$
$$+\frac{\sigma\sqrt{J}}{\sigma_{K}^{*}}\left(\tilde{\sigma}\sqrt{K\log d}+MB\log d\left\|\mathbf{V}^{*}\right\|_{2,\infty}+\sigma\sqrt{J}\left\|\mathbf{U}^{*}\right\|_{2,\infty} \right.$$
$$

$$
$$\left.+\sigma\sqrt{J}\left\|\mathbf{U}\mathbf{U}^{\top}\mathbf{U}^{*}-\mathbf{U}^{*}\right\|_{2,\infty}\right)$$
$$

$$
$$\lesssim\frac{\widetilde{\sigma}\sqrt{K\log d}\left(\sigma\sqrt{MN+J}+MB\log d\right)}{\sigma_{K}^{*}}+MB\log d\left\|\mathbf{V}\mathbf{V}^{\top}\mathbf{V}^{*}-\mathbf{V}^{*}\right\|_{2,\infty}$$
$$

$$
$$+\frac{\left(\sigma\sqrt{J}+MB\log d\right)MB\log d}{\sigma_{K}^{*}}\left\|\mathbf{V}^{*}\right\|_{2,\infty}$$
$$

$$
$$+\frac{\sigma\sqrt{J}\left(MB\log d+\sigma\sqrt{J}\right)}{\sigma_{K}^{*}}\left(\left\|\mathbf{U}^{*}\right\|_{2,\infty}+\left\|\mathbf{U}\mathbf{U}^{\top}\mathbf{U}^{*}-\mathbf{U}^{*}\right\|_{2,\infty}\right)$$
$$

$$
$$\lesssim\frac{\widetilde{\sigma}\sigma\sqrt{K\log d(MN+J)}}{\sigma_{K}^{*}}+MB\log d\left\|\mathbf{V}\mathbf{V}^{\top}\mathbf{V}^{*}-\mathbf{V}^{*}\right\|_{2,\infty}+\frac{\sigma MB\log d\sqrt{J}}{\sigma_{K}^{*}}\left\|\mathbf{V}^{*}\right\|_{2,\infty}$$
$$

$$
$$+\frac{\sigma^{2}J}{\sigma_{K}^{*}}\left(\left\|\mathbf{U}^{*}\right\|_{2,\infty}+\left\|\mathbf{U}\mathbf{U}^{\top}\mathbf{U}^{*}-\mathbf{U}^{*}\right\|_{2,\infty}\right),\tag{S.30}$$
$$

where the last inequality is from $ {MB}\log d \lesssim \sigma \sqrt{\left( {MN}\right) \land J} $ by (S.2) in Assumption S.3.

49
