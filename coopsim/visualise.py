import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.animation as animation

def save_animation(changes_all, videoname, plot_size_n):

    print("Running and saving animation")
    # 0 = stayed as D (red)
    # 1 = stayed as C (blue)
    # 2 = changed from D to C (green)
    # 3 = changed from C to D (yellow)
        
    cm = LinearSegmentedColormap.from_list("coopcols", ["red", "blue", "green", "yellow"], N= 4)

    def animate(i):
        #fig, ax = plt.subplots()
        ax.imshow(changes_all[i], cmap = cm, vmin=0, vmax=3)
        return fig, ax

    # Make video
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=1, metadata=dict(artist='Me'), bitrate=1800)

    fig, ax = plt.subplots(figsize=(plot_size_n, plot_size_n))
    plt.axis('off')
    anim = animation.FuncAnimation(fig, animate, frames=len(changes_all), blit=False)


    anim.save(videoname)
