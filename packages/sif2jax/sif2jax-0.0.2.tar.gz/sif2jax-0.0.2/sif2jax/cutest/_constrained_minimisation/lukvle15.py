import jax.numpy as jnp

from ..._problem import AbstractConstrainedMinimisation


class LUKVLE15(AbstractConstrainedMinimisation):
    """LUKVLE15 - Chained modified HS50 problem.

    Problem 5.15 from Luksan and Vlcek test problems.

    The objective is a chained modified HS50 function:
    f(x) = Σ[i=1 to (n-1)/4] [(x_{j+1} - x_{j+2})^2 + (x_{j+2} - x_{j+3})^2 +
                               (x_{j+3} - x_{j+4})^4 + (x_{j+4} - x_{j+5})^4]
    where j = 4(i-1), l = 4*div(k-1,3)

    Subject to equality constraints:
    c_k(x) = x_{l+1}^2 + 2x_{l+2} + 3x_{l+3} - 6 = 0, for k ≡ 1 (mod 3), 1 ≤ k ≤ n_C
    c_k(x) = x_{l+2}^2 + 2x_{l+3} + 3x_{l+4} - 6 = 0, for k ≡ 2 (mod 3), 1 ≤ k ≤ n_C
    c_k(x) = x_{l+3}^2 + 2x_{l+4} + 3x_{l+5} - 6 = 0, for k ≡ 0 (mod 3), 1 ≤ k ≤ n_C
    where n_C = 3(n-1)/4

    Starting point:
    x_i = 35.0 for i ≡ 1 (mod 4)
    x_i = 11.0 for i ≡ 2 (mod 4)
    x_i = 5.0 for i ≡ 3 (mod 4)
    x_i = -5.0 for i ≡ 0 (mod 4)

    Source: L. Luksan and J. Vlcek,
    "Sparse and partially separable test problems for
    unconstrained and equality constrained optimization",
    Technical Report 767, Inst. Computer Science, Academy of Sciences
    of the Czech Republic, 182 07 Prague, Czech Republic, 1999

    SIF input: Nick Gould, April 2001

    Classification: OOR2-AY-V-V
    """

    n: int = 9997  # Default dimension, (n-1) must be divisible by 4

    def objective(self, y, args):
        del args
        n = len(y)
        # Chained modified HS50 function - vectorized

        # We need groups of 5 consecutive elements starting at indices 0, 4, 8, ...
        num_groups = (n - 1) // 4
        if num_groups == 0:
            return jnp.array(0.0)

        # Create indices for the start of each group
        group_starts = jnp.arange(num_groups) * 4

        # We need to ensure we don't go out of bounds
        valid_groups = group_starts[group_starts + 4 < n]

        if len(valid_groups) == 0:
            return jnp.array(0.0)

        # Extract elements for all groups at once
        x_j1 = y[valid_groups]  # First element of each group
        x_j2 = y[valid_groups + 1]  # Second element
        x_j3 = y[valid_groups + 2]  # Third element
        x_j4 = y[valid_groups + 3]  # Fourth element
        x_j5 = y[valid_groups + 4]  # Fifth element

        # Compute all terms vectorized
        terms = (
            (x_j1 - x_j2) ** 2
            + (x_j2 - x_j3) ** 2
            + (x_j3 - x_j4) ** 4
            + (x_j4 - x_j5) ** 4
        )

        return jnp.sum(terms)

    def y0(self):
        # Starting point
        y = jnp.zeros(self.n)
        # x_i = 35.0 for i ≡ 1 (mod 4) -> 0-based: i ≡ 0 (mod 4)
        y = y.at[::4].set(35.0)
        # x_i = 11.0 for i ≡ 2 (mod 4) -> 0-based: i ≡ 1 (mod 4)
        y = y.at[1::4].set(11.0)
        # x_i = 5.0 for i ≡ 3 (mod 4) -> 0-based: i ≡ 2 (mod 4)
        y = y.at[2::4].set(5.0)
        # x_i = -5.0 for i ≡ 0 (mod 4) -> 0-based: i ≡ 3 (mod 4)
        y = y.at[3::4].set(-5.0)
        return y

    def args(self):
        return None

    def expected_result(self):
        # Solution pattern based on problem structure
        return None  # Unknown exact solution

    def expected_objective_value(self):
        return None  # Unknown exact objective value

    def bounds(self):
        return None

    def constraint(self, y):
        n = len(y)
        n_c = 3 * (n - 1) // 4

        if n_c == 0:
            return jnp.array([]), None

        # Based on S2MPJ implementation, constraints use direct indices:
        # For K=1,4,7,... (by 3):
        #   C(K) = E(K) + 2*X(K+1) + 3*X(K+2) - 6 = 0, where E(K) = X(K)^2
        #   C(K+1) = E(K+1) + 2*X(K+2) + 3*X(K+3) - 6 = 0, where E(K+1) = X(K+1)^2
        #   C(K+2) = E(K+2) + 2*X(K+3) + 3*X(K+4) - 6 = 0, where E(K+2) = X(K+2)^2
        # Note: All are equality constraints in LUKVLE15

        # Pad y to ensure we can access all required indices
        max_k = n_c
        max_idx = max_k + 4  # Maximum index needed
        if max_idx > n:
            padding = max_idx - n
            y = jnp.pad(y, (0, padding), mode="constant", constant_values=0)

        # Initialize constraints array
        constraints = jnp.zeros(n_c)

        # Process constraints in groups of 3
        for k in range(0, n_c, 3):
            # C(k): k ≡ 1 mod 3
            if k < n_c:
                c_k = y[k] ** 2 + 2 * y[k + 1] + 3 * y[k + 2] - 6
                constraints = constraints.at[k].set(c_k)

            # C(k+1): k+1 ≡ 2 mod 3
            if k + 1 < n_c:
                c_k1 = y[k + 1] ** 2 + 2 * y[k + 2] + 3 * y[k + 3] - 6
                constraints = constraints.at[k + 1].set(c_k1)

            # C(k+2): k+2 ≡ 0 mod 3
            if k + 2 < n_c:
                c_k2 = y[k + 2] ** 2 + 2 * y[k + 3] + 3 * y[k + 4] - 6
                constraints = constraints.at[k + 2].set(c_k2)

        return constraints, None
