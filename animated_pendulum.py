from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
plt.rcParams["animation.html"] = "html5"
import scipy.integrate as integrate
import matplotlib.animation as animation
from IPython.display import HTML
plt.rcParams.update({'font.size': 8, 'legend.fontsize': 8,
          'legend.handlelength': .25, 'legend.loc': 'upper right', 'legend.framealpha': 0.5}); 
#print(plt.style.available)
plt.style.use('seaborn-notebook')


class animated_pendulum:
    def __init__(self, fig, t, Ts, L, P1, P2, figtitle):
        self.t = t
        self.Ts = Ts
        self.samples = np.arange(0, len(self.t))
        self.P1 = P1
        self.P2 = P2
        self.P1x = L*sin(P1[0, :])
        self.P1y = -L*cos(P1[0, :])
        self.P2x = L*sin(P2[0, :])
        self.P2y = -L*cos(P2[0, :])

        self.fig = fig;
        sp = self.fig.suptitle(figtitle)
        sp.set_x(0.25)
        # Add subplot for pendulum swinging motion
        self.ax = self.fig.add_subplot(121, autoscale_on=False, xlim=(-2, 2), ylim=(-3, 1))
        self.ax.grid(); self.ax.axis('off'); self.ax.set_aspect('equal');
        # Add first true Pendulum
        self.line = Line2D(self.P1x, self.P1y, marker='o') 
        self.ax.add_line(self.line) 
        # Add second estimated/measured Pendulum
        self.line2 = Line2D(self.P2x, self.P2y, marker='o', color='0.5') 
        self.ax.add_line(self.line2)
        
        # Add subplot for Position Time series
        self.ax2 = self.fig.add_subplot(322, autoscale_on=False, xlim=(0, len(self.P1x)), ylim=(-3,3))
        self.ax2.set_title('Angular Position'); 
        self.ax2.set_ylabel('Radians'); self.ax2.set_xlabel('Time (k)'); 
        # Add first pendulum
        self.line3, = self.ax2.plot([],[], 'b', lw=4)
        # Add estimate/measure points 
        self.line4, = self.ax2.plot([],[], 'ro', ms=2.5, lw=0.25) # ms: marker size. lw: line width
        
        # Add subplot for Velocity Time series
        self.ax3 = self.fig.add_subplot(324, autoscale_on=False, xlim=(0, len(self.P1x)), ylim=(-3,3))
        self.ax3.set_title('Angular Velocity');
        self.ax3.set_ylabel('Radians/s'); self.ax3.set_xlabel('Time (k)'); 
        # Add first pendulum
        self.line5, = self.ax3.plot([],[], 'b', lw=4)
        # Add estimate/measure points 
        self.line6, = self.ax3.plot([],[], 'ro', ms=2.5, lw=0.25) # 
        
        # Add subplot for Velocity Time series
        self.ax4 = self.fig.add_subplot(326, autoscale_on=False, xlim=(0, len(self.P1x)), ylim=(-3,3))
        self.ax4.set_title('Estimate/Measurement Error');
        self.ax4.set_ylabel('Radians - Radians/s'); self.ax4.set_xlabel('Time (k)'); 
        # Add first pendulum
        self.line7, = self.ax4.plot([],[], 'b', lw=2)
        # Add estimate/measure points 
        self.line8, = self.ax4.plot([],[], 'g', lw=2)
        
        # At the end
        self.fig.tight_layout()

        
    # animation function. This is called sequentially
    def update(self, i):
        this1x = [0, self.P1x[i]]; this1y = [0, self.P1y[i]];
        this2x = [0, self.P2x[i]]; this2y = [0, self.P2y[i]];
        
        self.line.set_data(this1x, this1y); self.line.set_label('True'); 
        self.line2.set_data(this2x, this2y); self.line2.set_label('Estimate');
        label1 = self.ax.legend() # Legends must be rendered as well, not very legendary really. 
        self.line3.set_data(self.samples[:i], self.P1[0,:i]); self.line3.set_label('True'); 
        self.line4.set_data(self.samples[:i], self.P2[0,:i]); self.line4.set_label('Estimate');
        label2 = self.ax2.legend()
        self.line5.set_data(self.samples[:i], self.P1[1,:i]); self.line5.set_label('True'); 
        self.line6.set_data(self.samples[:i], self.P2[1,:i]); self.line6.set_label('Estimate');
        label3 = self.ax3.legend()
        self.line7.set_data(self.samples[:i], self.P1[0,:i] - self.P2[0,:i]); self.line7.set_label('Position'); 
        self.line8.set_data(self.samples[:i], self.P1[1,:i] - self.P2[1,:i]); self.line8.set_label('Velocity');
        label4 = self.ax4.legend()
        return self.line, self.line2, self.line3, self.line4, label1, label2, label3, label4


    def get_animation_video(self):
        ani = animation.FuncAnimation(self.fig, self.update, np.arange(1, len(self.P1x)), 
                                      interval=60, blit=True);
        
        return HTML(ani.to_html5_video());
