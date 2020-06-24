import math

import matplotlib.pyplot as plt

# =============
# constants
# =============

# gravity, meters/sec
g = 9.81
# air density, kg/m^3
r = 1.19183
# seconds
time_interval = 0.001
# deg
angles = range(5, 90, 5)

# =============
# parameters
# =============

# meters
starting_x = 0
starting_y = 1.55

# football
# =============
# meter/sec
power = 26.82
# kg
mass = 0.411
# coefficient
Cd = 0.0953
# m^2
A = 0.0248

# package data as dict
football = {"name": "football", "power": power, "mass": mass, "Cd": Cd, "A": A}

# corncob
# =============
# meter/sec
power = 39.413
# kg
mass = 0.279
# coefficient
Cd = 0.184
# m^2
A = 0.00098924

# package data as dict
corncob = {"name": "corncob", "power": power, "mass": mass, "Cd": Cd, "A": A}

# =============
# computations
# =============

items = [football, corncob]

for item in items:
    # unpack data
    name = item["name"]
    power = item["power"]
    mass = item["mass"]
    Cd = item["Cd"]
    A = item["A"]

    # terminal velocity
    V_t = math.sqrt((2 * mass * g) / (Cd * A * r))

    # create a new plot
    plt.figure()

    for angle_deg in angles:
        angle_rad = angle_deg * math.pi / 180

        U_0 = power * math.cos(angle_rad)
        V_0 = power * math.sin(angle_rad)

        pos_y = starting_y
        pos_x = starting_x

        time = 0

        x_vals = []
        y_vals = []

        while pos_y > 0:
            # https://www.grc.nasa.gov/www/k-12/airplane/Images/flteqs.gif
            pos_x = starting_x + (V_t ** 2 / g) * math.log(
                (V_t ** 2 + g * U_0 * time) / V_t ** 2
            )

            V = V_t * (
                (V_0 - V_t * math.tan(time * g / V_t))
                / (V_t + V_0 * math.tan(time * g / V_t))
            )
            pos_y = starting_y + (V_t ** 2 / (2 * g)) * math.log(
                (V_0 ** 2 + V_t ** 2) / (V ** 2 + V_t ** 2)
            )

            x_vals.append(pos_x)
            y_vals.append(pos_y)

            time += time_interval

        print(
            "Thrown at {} degrees, a {} will fly for {} seconds, "
            "landing {} meters downfield.".format(
                angle_deg, name, round(time, 2), round(pos_x, 2)
            )
        )

        plt.plot(x_vals, y_vals, label="{} deg".format(angle_deg))

    plt.title("Angle vs {} Distance".format(name.title()))
    plt.ylabel("Height (m)")
    plt.xlabel("Distance (m)")

    plt.ylim(bottom=0)
    plt.grid()
    plt.legend()

    print("==========================")

# when done, show plot
plt.show()
