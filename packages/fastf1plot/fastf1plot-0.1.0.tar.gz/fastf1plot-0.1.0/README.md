# F1_lap_time_telementary

A Python module to plot telemetry data from Formula 1 sessions using FastF1.

## Usage

```python
from fastf1plot import plot_comparison

plot_comparison(
    year=2025,
    grand_prix='Chinese Grand Prix',
    session_type='Q',
    drivers=['ALO', 'STR']
)
