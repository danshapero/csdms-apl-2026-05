---
title: Glacier flow modeling
---

## Modeling glacier flow

<img src="IMG20240722183306.jpg" width="60%">

Daniel Shapero, shapero@uw.edu

-v-

### Overview

* Glacier flow, in broad strokes
* Terminus advance and retreat with duality
* Stokes flow in terrain-following coordinates



---

### Glacier flow

-v-

### Why study glaciers

<img src="https://www.nps.gov/articles/000/images/MORA-Stream-Temp_Fig1_web.jpeg?maxwidth=1300&autorotate=false&quality=78&format=webp" width="80%">

<small>Emmons Glacier on Mt. Rainier and the White River, from NPS</small>

-v-

### Broad strokes

* You can think of glaciers as a **thin film** of **viscous** fluid, flowing by **gravity**.
* Other viscous gravity currents in the earth sciences: rainfall runoff, lava flows, debris flows.
* Ice is unusual because of **rheology**, **bed sliding**, and **iceberg calving**.

-v-

show velocity map of Antarctica

-v-

<iframe width="840" height="472" src="https://www.youtube.com/embed/YslhQZwvvu0?si=0e8BimEQXFGMc002?rel=0&modestbranding=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<small>Malaspina Glacier, Alaska. From Bas Altena</small>

-v-

### Mass conservation

* Glacier ice is nearly incompressible:
$$\nabla\cdot u = 0.$$
* We can integrate this in $z$ to get an evolution equation for the ice thickness $h$:
$$\frac{\partial h}{\partial t} + \underbrace{\nabla\cdot h\bar u}\_{\text{flux}} = \underbrace{\dot a}\_{\text{accum}} - \underbrace{\dot m}\_{\text{melt}}$$

-v-

### Momentum conservation

* Reynolds number is super low:
$$\begin{align\*}
& \bcancel{\cancel{\frac{\partial}{\partial t}\rho u + \nabla\cdot \rho u\otimes u}} \\\\
& \qquad = \underbrace{\nabla\cdot\tau}\_{\text{viscosity}} - \underbrace{\nabla p}\_{\text{pressure}} + \underbrace{\rho g}\_{\text{gravity}}
\end{align\*}$$
* To close the system, we need a constitutive relation and boundary conditions.

-v-

### The Glen flow law

* For fluids, we care about the strain rate:
$$\dot\varepsilon = \frac{1}{2}\left(\nabla u + \nabla u^\*\right)$$
* For a Newtonian fluid, stress $\sim$ strain rate:
$$\underbrace{\tau}\_{\text{stress}} = 2\times\underbrace{\mu}\_{\text{viscosity}}\times\underbrace{\dot\varepsilon}\_{\text{strain rate}}$$
**Glaciers are not Newtonian**.

-v-

### The Glen flow law

* Glacier flow is *shear-thinning*.
* Laboratory experiments in the 50s showed that
$$\dot\varepsilon = A|\tau|^{n - 1}\tau$$
where $n$ is somewhere between 3 and 4.
* Missing pieces: sum of several powers, anisotropy.

-v-

figure showing Raymond arches

-v-

### The sliding law

* Ice slides over its bed.
Friction is also a power law:
$$u = -K|\tau\_b|^{m - 1}\tau\_b$$
* Missing pieces: dependence on bedrock geology and hydrology

-v-

figure showing chatter marks or lineations

-v-

### Minimization principle

$\cdot$

$$\begin{align\*}
L(u, p) & = \int\_\Omega\left(\frac{2n}{n + 1}A^{-\frac{1}{n}}|\dot\varepsilon|^{\frac{1}{n} + 1} - p\nabla\cdot u - \rho g\cdot u\right)\mathrm dx \\\\
& \qquad\qquad + \int\_\Gamma\frac{m}{m + 1}K^{-\frac{1}{m}}|u|^{\frac{1}{m} + 1}\mathrm d\gamma
\end{align\*}$$



---

### Approximations

-v-

### Thin-film flow

* Most glaciers are much thinner than they are wide.
* Simplifies the $z$-component of the Stokes eqns:
$$\bcancel{\cancel{\partial\_x\tau\_{zx}}} + \bcancel{\cancel{\partial\_y\tau\_{zy}}} + \partial\_z\left(\tau\_{zz} - p - \rho g (s - z)\right) = 0$$
$\Rightarrow$ we can eliminate the pressure.

-v-

### The first-order equations

* We get a system of equations for just the horizontal velocity components $u$, $v$ in 3D.
* These are called the *first-order* equations.
* Q: Can we simplify out the $z$-dimension?
* A: **Yes, in two different ways!**

-v-

### The shallow ice approximation

* Assumption: ice is nearly frozen to the bed and the vertical shear modes $\dot\varepsilon\_{xz}$, $\dot\varepsilon\_{yz}$ are dominant.
* Consequence: **depth-averaged velocity is a function of the local thickness and surface slope**.

$$\begin{align\*}
\text{driving stress}: \quad \tau\_d & = -\rho gh\nabla s \\\\
\text{velocity}: \quad \bar u & = \frac{2hA}{n + 2}|\tau\_d|^{n - 1}\tau\_d
\end{align\*}$$

-v-

### The shallow ice approximation

* The good:
  - Simple to code.
  - **The model still works fine even when $h = 0$.**
* The bad:
  - Can't handle floating ice.
  - Assumes $\bar u \sim -\nabla s$ but DEMs are noisy.
  - Allstadt (2015): SIA can reproduce only 5\% of the speed of Emmons Glacier.

-v-

show a simulation of a synthetic case with SIA

-v-

### The shallow stream approximation

* Assumption: ice flow is by horizontal extension; $\dot\varepsilon\_{xx}$, $\dot\varepsilon\_{yy}$, $\dot\varepsilon\_{xy}$ are dominant.
* Depth-average velocity now solves a PDE.
* Can handle floating ice + fast flow.
* **The model doesn't work when $h = 0$.**

-v-

### SSA

* When we go to 1st-order model, the natural choice is to work with the *membrane stress tensor*
$$M = \left[\begin{matrix}\tau\_{xx} & \tau\_{xy} \\\\ \tau\_{yx} & \tau\_{yy}\end{matrix}\right] + (\tau\_{xx} + \tau\_{yy})\left[\begin{matrix} 1 & 0 \\\\ 0 & 1\end{matrix}\right]$$
* This is what's left over when we eliminate the pressure and normal stress.

-v-

### SSA

* The constitutive relation now looks like
$$M = 2\mu\left\\{\dot\varepsilon + \text{tr}(\dot\varepsilon)I\right\\}.$$
* We can also write this as
$$M = 2\mu\mathscr C\dot\varepsilon$$
where $\mathscr C$ is some funny rank-4 tensor.

-v-

### SSA

* We get a conservation law for membrane stress:
$$\underbrace{\nabla\cdot hM}\_{\text{viscosity}} + \underbrace{\tau\_b}\_{\text{friction}} - \underbrace{\rho gh\nabla s}\_{\text{gravity}} = 0$$
* Much easier to solve than Stokes or 1st-order!

-v-

### Minimization principle for SSA

$$\begin{align\*}
& J(u) = \int\_\Omega\Bigg(\frac{2n}{n + 1}hA^{-\frac{1}{n}}|\dot\varepsilon|\_{\mathscr C}^{\frac{1}{n} + 1} \\\\
& \qquad\qquad\qquad + \frac{m}{m + 1}K^{-\frac{1}{m}}|u|^{\frac{1}{m} + 1} + \rho gh\nabla s\cdot u\Bigg)\mathrm dx
\end{align\*}$$

-v-

show velocity map of Antarctica, draw where SIA / SSA are good

-v-

show some result obtained with SSA

-v-

### Summary

show the diagram



---

### Terminus evolution

-v-

<iframe width="840" height="472" src="https://www.youtube.com/embed/TWGR6FxFlt8?si=rTZGByPomHoLMCWy?rel=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<small>LeConte Glacier, Alaska. From Christian Kienholz</small>

-v-

### The dilemma

* SIA can deal with moving termini, SSA can't.
* SSA can capture glacier velocity, SIA can't.
* **Can we obtain the best of both?**

-v-

### Terminus advance/retreat

- Terminus evolution = a free boundary problem!
- **Problem**: when $h = 0$, bad things happen.
- **Solutions**:
  - low-order FV discretization (BISICLES)
  - level-set methods (ISSM)
  - remeshing (Elmer/ICE)

-v-

### Why is this a problem?

* The thing we want to minimize:
$$J(u) = \int_\Omega\left(\ldots h\cdot |\dot\varepsilon|^{4/3}\ldots\right)\mathrm dx$$
* When $h \to 0$, $\dot\varepsilon \to 0$ too.
* So the curvature of $J$ looks like $0 \times \infty$!

-v-

### Convex duality

* Both Stokes and SSA have minimization principles.
* **Every convex minimization problem has a twin.**
* Solving the primal problem is an upper bound for the dual and vice versa.

-v-

### Convex duality

* Example: linear elasticity.
Find a \_\_\_ that minimizes the elastic energy.
  - primal problem: displacement
  - dual problem: stress tensor
* Why should we care?
  - More accurate approximation of stress
  - **Inverts all constitutive relations**

-v-

### The dual of SSA

$$\begin{align\*}
& L = \int\_\Omega\Bigg\\{\frac{2}{n + 1}hA|M|\_{\mathscr A}^{n + 1} + \frac{1}{m + 1}K|\tau|^{m + 1}  \\\\
& \qquad\qquad\qquad - h M :\dot\varepsilon + \tau\cdot u - \rho gh\nabla s\cdot u \Bigg\\}\mathrm dx
\end{align\*}$$

-v-

### Larsen C simulation

-v-

### Emmons Glacier



---

### Stokes flow in terrain-following coordinates

-v-

### Stokes flow

* 2D models are nice but sometimes you want "ground truth".
* The orthodox approach: a moving mesh.
* An alternative: a moving *coordinate system*.

-v-

### Terrain-following coordinates

* Use a new coordinate $\zeta$ such that
$$z = b(x, y) + h(x, y, t)\cdot\zeta.$$
* The vertical domain is now just the interval $[0, 1]$.
* Integrals pick up a factor of $h$:
$$\mathrm dz \mapsto h\\,\mathrm d\zeta$$

-v-

### Terrain-following coordinates

* Taking a derivative w.r.t. $x$ with $z$ fixed is not the same as with $\zeta$ fixed!
* Let $J = \mathrm dx/\mathrm d\xi$; a few things change:
$$u\_x = J\cdot u\_\xi$$
$$\nabla\_x\phi = \nabla\_\xi\phi\cdot J^{-1}$$

-v-

### Terrain-following coordinates

show a drawing to illustrate

-v-

### Terrain-following coordinates

* **The problem**: if we discretize $h$, then $J$ jumps across cell boundaries.
* But it lives under a derivative:
$$\nabla\_x u\_x = \nabla\_\xi(Ju\_\xi)J^{-1}!$$
