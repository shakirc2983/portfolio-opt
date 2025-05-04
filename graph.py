import numpy as np
import matplotlib.pyplot as plt

# Set basic parameters
rf = 0.03  # Risk-free rate
sigma_m = 0.15  # Std deviation of the market portfolio
r_m = 0.12  # Return of the market portfolio

# Efficient Frontier (only risky assets)
sigma_ef = np.linspace(0.05, 0.3, 100)
# A realistic upward sloping concave shape (inverted parabola)
r_ef = -0.5 * (sigma_ef - sigma_m)**2 + r_m  # Peaks at (sigma_m, r_m)

# Capital Market Line (tangent to the efficient frontier at Market Portfolio)
sigma_cml = np.linspace(0, 0.3, 100)
r_cml = rf + (r_m - rf) / sigma_m * sigma_cml  # Straight line from rf through (sigma_m, r_m)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(sigma_ef, r_ef, label='Efficient Frontier', color='blue', linewidth=2)
plt.plot(sigma_cml, r_cml, label='Capital Market Line (CML)', color='black', linewidth=2)

# Risk-free rate point
plt.scatter(0, rf, color='black')
plt.text(0.01, rf, 'Risk-Free Rate', verticalalignment='bottom')

# Market Portfolio
plt.scatter(sigma_m, r_m, color='cyan', edgecolor='black', s=100, zorder=5)
plt.text(sigma_m + 0.01, r_m, 'Ideal Market Portfolio', color='teal', fontsize=12, verticalalignment='bottom')

# Inferior assets (randomly placed below efficient frontier)
inferior_sigmas = np.random.uniform(0.05, 0.25, 6)
inferior_returns = r_ef[np.searchsorted(sigma_ef, inferior_sigmas)] - np.random.uniform(0.01, 0.03, 6)
plt.scatter(inferior_sigmas, inferior_returns, color='dodgerblue', alpha=0.6, label='Inferior Portfolios & Assets')

# Labels and grid
plt.xlabel('Expected Risk (Standard Deviation)')
plt.ylabel('Expected Return')
plt.title('Capital Market Line & Efficient Frontier (CAPM)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()