---
title: Glacier flow modeling
---

## Modeling glacier flow

<img src="IMG20240722183306.jpg" width="60%">

Daniel Shapero, shapero@uw.edu

-v-

### Overview

* Introduction and how I got here
* Glacier flow, in broad strokes
* Terminus advance and retreat with duality
* Stokes flow in terrain-following coordinates


---

### Introduction

I solve differential equations for money

-v-

### Why study glaciers

<img src="https://www.nps.gov/articles/000/images/MORA-Stream-Temp_Fig1_web.jpeg?maxwidth=1300&autorotate=false&quality=78&format=webp" width="80%">

<small>Emmons Glacier on Mt. Rainier and the White River, from NPS</small>

-v-

### Broad strokes

* You can think of glaciers as a **thin film** of **viscous** fluid, flowing under **gravity**.
* Other viscous gravity currents in the earth sciences: rainfall runoff, lava flows, debris flows.
* Ice is unusual because of **rheology**, **bed sliding**, and **iceberg calving**.

-v-

### Some history

* I started an applied math PhD at UW in 2010.
* My degree prepared me to solve PDEs real fast.
* **Physical scientists are not limited by speed first.**

-v-

<img src="https://icepack.github.io/images/logo.svg">

**Goal**: make simulating glaciers easier and more interactive.

-v-

<center><img src="https://www.firedrakeproject.org/_static/banner.png"></center>

Built on Firedrake, a Python package for solving PDEs.

Specify the PDE using a *domain-specific language*.


---

### Glacier flow

-v-

<small>InSAR-based velocity map of Antarctica from NSIDC</small>

<center><img src=https://nsidc.org/sites/default/files/images/satellite-aiv-velocity-magnitude.png width="60%"></center>

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

### Raymond arches

<center><img src="raymond-1983.png" width="60%"></center>

Simulated streamlines of flow near divide of Devon Island Ice Cap from Raymond (1983), *Deformation in the vicinity of ice divides*.

-v-

### Raymond arches

<div class="multicolumn">

<div>

<center><img src="vaughan-1999.png" width="60%"></center>

</div>

<div>

Radargram from Vaughan et al. (1999), *Distortion of isochronous layers revealed by ground-penetrating radar*.

Some of the best field evidence we have for the Glen flow law.

</div>

</div>

-v-

### Boundary conditions

* Notation: $\parallel$ = parallel, $\perp$ = perpendicular
* At the surface, stress is zero:
$$(\tau - pI)\_\parallel = 0 \quad \text{at } z = z\_s$$
* At the base, velocity is equal to the melt rate:
$$u\_\parallel = \dot m \quad \text{at } z = z\_b$$
**What about friction?**

-v-

### Sliding law

* Friction is (maybe?) a power law:
$$u\_\perp = -K|\tau\_b|^{m - 1}\tau\_b$$
* The basal BC type depends on the direction!
* Missing pieces: hydrology, geology

-v-

### Sliding law

<center><img src="https://www.antarcticglaciers.org/wp-content/uploads/2019/09/Dubawnt-Lake-MSGLs-1024x622.png" width="65%"></center>

<small>

From Stokes and Clark (2003), *The Dubawnt Lake palaeo-ice stream: evidence for dynamic ice sheet behavior on the Canadian shield*

</small>

-v-

### Summary

* Momentum balance is:
  - conservation law
  - flow law${}^{-1}$ (stress $\sim$ strain rate${}^{1/n}$)
  - sliding law${}^{-1}$ (drag $\sim$ speed${}^{1/m}$)
  - fixed normal velocity at the base
  - no stress at the surface
* Throw it all at a finite element solver and pray, right?

-v-

### Minimization principle

* The Stokes problem can also be derived through minimizing the *free energy dissipation rate*.
* Minimization principles are *awesome* for numerics.

-v-

### Minimization principle

$$\begin{align\*}
\dot F(u, p) & = \int\_\Omega\left(\frac{2n}{n + 1}A^{-\frac{1}{n}}|\dot\varepsilon|^{\frac{1}{n} + 1} - p\nabla\cdot u - \rho g\cdot u\right)\mathrm dx \\\\
& \qquad\qquad + \int\_\Gamma\frac{m}{m + 1}K^{-\frac{1}{m}}|u\_\perp|^{\frac{1}{m} + 1}\mathrm d\gamma
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

* A conservation law for *membrane stress* $M$:
$$\underbrace{\nabla\cdot hM}\_{\text{viscosity}} + \underbrace{\tau\_b}\_{\text{friction}} - \underbrace{\rho gh\nabla s}\_{\text{gravity}} = 0$$
* Much easier to solve than Stokes or 1st-order!
* Also has a minimization principle.

-v-

<center><img src=https://nsidc.org/sites/default/files/images/satellite-aiv-velocity-magnitude.png width="60%"></center>

-v-

show some result obtained with SSA

-v-

### Approximations

<center>
<div class="mermaid">
%%{init: {
    'theme': 'light'
}%%
flowchart TD
    A[Stokes] -- "thin film" --> B[First-order];
    B -- "vertical shear" --> C[SIA];
    B -- "plug flow" --> D[SSA];

</div>
</center>



---

### Terminus evolution

-v-

<iframe width="840" height="472" src="https://www.youtube.com/embed/TWGR6FxFlt8?si=rTZGByPomHoLMCWy?rel=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

<small>LeConte Glacier, Alaska. From Christian Kienholz</small>

-v-

### The dilemma

<div class="multicolumn">

<div>

* SIA can move termini, SSA can't.
* SSA can capture velocity, SIA can't.
* **Can we obtain the best of both?**

</div>

<div>

<center>
<div class="mermaid">
%%{init: {
    'theme': 'light'
}%%
flowchart TD
    A[Stokes] -- "thin film" --> B[First-order];
    B -- "vertical shear" --> C[SIA];
    B -- "plug flow" --> D[SSA];
    C --> E[?];
    D --> E;

</div>
</center>

</div>

</div>

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
$$\dot F = \int_\Omega\left(\ldots h\cdot |\dot\varepsilon|^{4/3}\ldots\right)\mathrm dx$$
* When $h \to 0$, $\dot\varepsilon \to 0$ too.
* So the curvature looks like $0 \times \infty$!

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

### The dual form of Stokes

$$\begin{align\*}
& \dot F = \int\_\Omega\left\\{\frac{2}{n + 1}A|\tau|^{n + 1} - \tau : \dot\varepsilon + p\nabla\cdot u + \rho g\cdot u\right\\}\mathrm dx  \\\\
& \qquad\qquad + \int\_\Gamma\left\\{\frac{1}{m + 1}K|\tau_\perp|^{m + 1} + \tau\_\perp\cdot u\_\perp\right\\}\mathrm d\gamma
\end{align\*}$$

-v-

### The dual form of Stokes

* Strain rate${}^{4/3}$ becomes stress${}^4$ -- no more cusp!
* Add terms to get composite flow / sliding laws.
* **The dual form of SSA is solvable at $h = 0$.**

-v-

### Larsen C simulation

<center><iframe width="600" height="350" data-src="https://www.youtube.com/embed/qq6lw7D9NR0?rel=0" frameborder="0" allowfullscreen></iframe></center>

<small>

From Shapero and de Diego (2025), *Numerical simulation of glacier terminus evolution using the dual action principle for momentum balance*

</small>

-v-

### Emmons Glacier

<center><iframe width="600" height="350" data-src="https://www.youtube.com/embed/RZO1fnDV3-w?rel=0" allowfullscreen></iframe></center>

<small>By my student Jon Maurer</small>

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

* **The problem**: if we discretize $h$ with finite elements, then $J$ jumps across facets.
* But it lives under a derivative:
$$\nabla\_x u\_x = \nabla\_\xi(Ju\_\xi)J^{-1}!$$



---

### Conclusion

-v-

### Future work

* **Firn**: densification of snow into ice
* **Heat flow**: phase change
* **Fabric**: crystal anisotropy and mechanics
* **Damage mechanics**: try new calving laws
* **Inverse problems**: estimating thickness, friction, viscosity from remote sensing data

-v-

### Conclusion

I will solve differential equations for money

<center>

**shapero@uw.edu**

</center>
