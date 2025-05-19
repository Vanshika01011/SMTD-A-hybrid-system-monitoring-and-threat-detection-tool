##                                  Graph switching via dropdown menu




import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import psutil
import time
from collections import deque

class LiveGraphFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.selected_metric = tk.StringVar(value="All")

        self.cpu_data = deque([0]*60, maxlen=60)
        self.ram_data = deque([0]*60, maxlen=60)
        self.disk_data = deque([0]*60, maxlen=60)
        self.net_data = deque([0]*60, maxlen=60)

        self.last_net = psutil.net_io_counters()
        self.last_time = time.time()

        dropdown_frame = ttk.Frame(self)
        dropdown_frame.pack(pady=5)
        ttk.Label(dropdown_frame, text="Select Metric: ").pack(side="left")
        metric_options = ["All", "CPU", "Memory", "Disk", "Network"]
        self.metric_selector = ttk.Combobox(dropdown_frame, textvariable=self.selected_metric, values=metric_options, state="readonly")
        self.metric_selector.pack(side="left")
        self.metric_selector.bind("<<ComboboxSelected>>", lambda e: self.update_plot_visibility())

        self.fig, self.ax1 = plt.subplots(figsize=(8, 4), dpi=100)
        self.ax2 = self.ax1.twinx()

        self.line_cpu, = self.ax1.plot([], [], label='CPU %', color='tab:blue')
        self.line_ram, = self.ax1.plot([], [], label='RAM %', color='tab:green')
        self.line_disk, = self.ax1.plot([], [], label='Disk %', color='tab:orange')
        self.line_net, = self.ax2.plot([], [], label='Network (KB/s)', color='tab:red', linestyle='--')

        self.ax1.set_ylim(0, 100)
        self.ax1.set_xlim(0, 60)
        self.ax2.set_ylim(0, 1000)

        self.ax1.set_title("Real-Time Resource Usage")
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("CPU / RAM / Disk (%)")
        self.ax2.set_ylabel("Network (KB/s)")

        self.ax1.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.ani = FuncAnimation(self.fig, self.update_graph, interval=1000)

    def update_plot_visibility(self):
        metric = self.selected_metric.get()
        self.line_cpu.set_visible(metric in ("All", "CPU"))
        self.line_ram.set_visible(metric in ("All", "Memory"))
        self.line_disk.set_visible(metric in ("All", "Disk"))
        self.line_net.set_visible(metric in ("All", "Network"))
        self.ax1.legend(loc="upper right")
        self.canvas.draw()

    def update_graph(self, i):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        current_net = psutil.net_io_counters()
        current_time = time.time()
        delta_time = current_time - self.last_time

        bytes_sent = current_net.bytes_sent - self.last_net.bytes_sent
        bytes_recv = current_net.bytes_recv - self.last_net.bytes_recv
        net_speed_kb = (bytes_sent + bytes_recv) / 1024 / delta_time

        self.last_net = current_net
        self.last_time = current_time

        self.cpu_data.append(cpu)
        self.ram_data.append(ram)
        self.disk_data.append(disk)
        self.net_data.append(net_speed_kb)

        self.line_cpu.set_data(range(len(self.cpu_data)), list(self.cpu_data))
        self.line_ram.set_data(range(len(self.ram_data)), list(self.ram_data))
        self.line_disk.set_data(range(len(self.disk_data)), list(self.disk_data))
        self.line_net.set_data(range(len(self.net_data)), list(self.net_data))

        self.ax1.set_xlim(0, len(self.cpu_data))
        self.ax2.set_xlim(0, len(self.cpu_data))

        max_net = max(self.net_data)
        self.ax2.set_ylim(0, max(500, max_net * 1.5))

        self.update_plot_visibility()

class SMTDApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Monitoring and Threat Detection Tool - SMTD")
        self.geometry("900x500")
        LiveGraphFrame(self).pack(fill="both", expand=True)

if __name__ == '__main__':
    app = SMTDApp()
    app.mainloop()