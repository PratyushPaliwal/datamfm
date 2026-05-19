# The Product Rule

If we divide by $\Delta x$, we get

$$
$$
\frac { \Delta ( u v ) } { \Delta x } = u \frac { \Delta v } { \Delta x } + v \frac { \Delta u } { \Delta x } + \Delta u \frac { \Delta v } { \Delta x }
$$
$$

If we now let $\Delta x \to 0$, we get the derivative of $uv$:

$$
$$
\begin{align*}
\frac{d}{dx}(uv) &= \lim_{\Delta x \to 0} \frac{\Delta(uv)}{\Delta x} = \lim_{\Delta x \to 0} \left( u \frac{\Delta v}{\Delta x} + v \frac{\Delta u}{\Delta x} + \Delta u \frac{\Delta v}{\Delta x} \right) \\[2em]
&= u \lim_{\Delta x \to 0} \frac{\Delta v}{\Delta x} + v \lim_{\Delta x \to 0} \frac{\Delta u}{\Delta x} + \left( \lim_{\Delta x \to 0} \Delta u \right) \left( \lim_{\Delta x \to 0} \frac{\Delta v}{\Delta x} \right) \\[2em]
&= u \frac{dv}{dx} + v \frac{du}{dx} + 0 \cdot \frac{dv}{dx}
\end{align*}
$$
$$

7
