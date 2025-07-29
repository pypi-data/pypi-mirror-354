# fastf1_plot_api.py

import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt


def setup_plotting():
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False,
                               color_scheme='fastf1')


def get_session_data(year, gp, session_type):
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    return session


def get_driver_data(session, driver):
    lap = session.laps.pick_drivers(driver).pick_fastest()
    car_data = lap.get_car_data().add_distance()
    return lap, car_data


def get_min_max_speed(car_data):
    return car_data['Speed'].min(), car_data['Speed'].max()


def plot_corners(ax, circuit_data, vmin, vmax):
    ax.vlines(
        x=circuit_data.corners['Distance'],
        ymin=vmin - 20,
        ymax=vmax + 20,
        linestyles='dotted',
        colors='grey'
    )
    for _, corner in circuit_data.corners.iterrows():
        label = f"{corner['Number']}{corner['Letter']}"
        ax.text(corner['Distance'], vmin - 30, label,
                va='center_baseline', ha='center', size='small')


def plot_telemetry(axs, car_data, label):
    axs[0].plot(car_data['Distance'], car_data['Speed'], label=label)
    axs[1].plot(car_data['Distance'], car_data['Throttle'], label=label)
    axs[2].plot(car_data['Distance'], car_data['Brake'], label=label)
    axs[3].plot(car_data['Distance'], car_data['nGear'], label=label)


def label_axes(axs):
    labels = ['Speed [km/h]', 'Throttle [%]', 'Brake [%]', 'Gear']
    for ax, label in zip(axs, labels):
        ax.set_ylabel(label)
    axs[-1].set_xlabel('Distance [m]')


def add_legends(axs):
    for ax in axs:
        ax.legend()


def set_title(axs, title):
    axs[0].set_title(title)


def plot_comparison(year, grand_prix, session_type, drivers):
    setup_plotting()
    session = get_session_data(year, grand_prix, session_type)
    circuit_data = session.get_circuit_info()

    fig, axs = plt.subplots(4, 1, sharex=True, figsize=(10, 10))

    vmin, vmax = float('inf'), float('-inf')
    driver_data = {}

    for driver in drivers:
        lap, car_data = get_driver_data(session, driver)
        driver_data[driver] = (lap, car_data)

        drv_min, drv_max = get_min_max_speed(car_data)
        vmin, vmax = min(vmin, drv_min), max(vmax, drv_max)

    plot_corners(axs[0], circuit_data, vmin, vmax)

    for driver in drivers:
        lap, car_data = driver_data[driver]
        plot_telemetry(axs, car_data, lap['Driver'])

    label_axes(axs)
    add_legends(axs)

    # Generate the title dynamically
    session_map = {
        'FP1': 'Free Practice 1',
        'FP2': 'Free Practice 2',
        'FP3': 'Free Practice 3',
        'SQ': 'Sprint Qualifying',
        'SS': 'Sprint Shootout', #2023 only
        'Q': 'Qualifying',
        'S': 'Sprint',
        'R': 'Race'
    }

    session_str = session_map.get(session_type.upper(), session_type)
    title = f"{' vs '.join(drivers)} - {year} {grand_prix} {session_str}"
    set_title(axs, title)

    plt.tight_layout()
    plt.show()