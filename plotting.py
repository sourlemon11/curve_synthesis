""" Plotting """
import matplotlib.pyplot as mpl
from matplotlib.widgets import Slider, Button, RadioButtons
# %matplotlib gtk3
logging.debug("---------------------------Plotting---------------------------")

fig, ax = mpl.subplots()
mpl.subplots_adjust(left=0.25, bottom=0.25)

# Main constraint circle
# Initial coord
# logging.debug(f"{C_motion_all_t.x[0]}")
# logging.debug(f"{C_motion_all_t.y[0]}")
handle_plot, = ax.plot(C_motion_all_t.x[0],
                       C_motion_all_t.y[0],
                       lw=2)

# Plot all Idler pts throughout rotation around center
for i in range(Idler_Motion_Pts.Vars['t'].linspace.size):
    ax.plot(Idler_Motion_Pts.x[i][:], Idler_Motion_Pts.y[i][:])

mpl.xlim(Idler_Motion_Pts.x_lim)
mpl.ylim(Idler_Motion_Pts.y_lim)
mpl.xlabel('x')
mpl.ylabel('y')

mpl.grid()
mpl.gca().set_aspect('equal', adjustable='box')

## Plot constant tValues along f(t, thetaSpace)

# Color
axcolor = 'lightgoldenrodyellow'
ax_θ_O = mpl.axes([0.25, 0.1, 0.5, 0.05], facecolor=axcolor)

sliθ_O = mpl.Slider(ax_θ_O, 'θ_O (Rotation Around P_0)', Omega_O.linspace[0], Omega_O.linspace[-1])
sliθ_O.set_val(C_motion_all_t.Vars['omega_O'].val)

def update(val):
    C_motion_all_t.Vars['omega_O'].val = val
    C_motion_all_t.coord_gen()

    handle_plot.set_xdata(C_motion_all_t.x[-1])
    handle_plot.set_ydata(C_motion_all_t.y[-1])
    fig.canvas.draw_idle()

sliθ_O.on_changed(update)

mpl.show()
