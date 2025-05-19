##                                    Optimize resource usage & refresh intervals 


import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import psutil
import time
from collections import deque
import threading

class LiveGraphFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.selected_metric = tk.StringVar(value="All")
        self.refresh_rate = tk.IntVar(value=2000)
        self.is_paused = tk.BooleanVar(value=False)

        self.cpu_data = deque([0]*60, maxlen=60)
        self.ram_data = deque([0]*60, maxlen=60)
        self.disk_data = deque([0]*60, maxlen=60)
        self.net_data = deque([0]*60, maxlen=60)

        self.last_net = psutil.net_io_counters()
        self.last_time = time.time()

        control_frame = ttk.Frame(self)
        control_frame.pack(pady=5)

        ttk.Label(control_frame, text="Select Metric: ").pack(side="left")
        metric_options = ["All", "CPU", "Memory", "Disk", "Network"]
        self.metric_selector = ttk.Combobox(control_frame, textvariable=self.selected_metric, values=metric_options, state="readonly", width=10)
        self.metric_selector.pack(side="left", padx=5)
        self.metric_selector.bind("<<ComboboxSelected>>", lambda e: self.update_plot_visibility())

        ttk.Label(control_frame, text="Refresh: ").pack(side="left", padx=5)
        self.interval_selector = ttk.Combobox(control_frame, values=[1000, 2000, 5000, 10000], textvariable=self.refresh_rate, state="readonly", width=5)
        self.interval_selector.pack(side="left")
        self.interval_selector.bind("<<ComboboxSelected>>", lambda e: self.change_interval())

        self.pause_button = ttk.Button(control_frame, text="⏸ Pause", command=self.toggle_pause)
        self.pause_button.pack(side="left", padx=5)

        self.fig, self.ax1 = plt.subplots(figsize=(6, 3), dpi=80)
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

        self.ani = FuncAnimation(
            self.fig, self.update_graph, interval=self.refresh_rate.get(), blit=True, cache_frame_data=False
        )

    def change_interval(self):
        self.ani.event_source.interval = self.refresh_rate.get()

    def toggle_pause(self):
        self.is_paused.set(not self.is_paused.get())
        self.pause_button.config(text="▶ Resume" if self.is_paused.get() else "⏸ Pause")

    def update_plot_visibility(self):
        metric = self.selected_metric.get()
        self.line_cpu.set_visible(metric in ("All", "CPU"))
        self.line_ram.set_visible(metric in ("All", "Memory"))
        self.line_disk.set_visible(metric in ("All", "Disk"))
        self.line_net.set_visible(metric in ("All", "Network"))
        self.ax1.legend(loc="upper right")
        self.canvas.draw()

    def update_graph(self, i):
        if self.is_paused.get():
            return []

        cpu = psutil.cpu_percent(percpu=False)
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
        visible_lines = [line for line in [self.line_cpu, self.line_ram, self.line_disk, self.line_net] if line.get_visible()]
        return visible_lines

class ProcessViewerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Running Processes", font=("Segoe UI", 12, "bold")).pack(pady=5)

        search_frame = ttk.Frame(self)
        search_frame.pack(pady=5)
        ttk.Label(search_frame, text="Search: ").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<KeyRelease>", self.debounced_search)

        columns = ("pid", "name", "cpu", "memory")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("pid", text="PID")
        self.tree.heading("name", text="Name")
        self.tree.heading("cpu", text="CPU %")
        self.tree.heading("memory", text="Memory %")

        for col in columns:
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        kill_btn = ttk.Button(self, text="Kill Selected Process", command=self.kill_selected_process)
        kill_btn.pack(pady=5)

        self.search_job = None
        self.update_processes_threaded()

    def debounced_search(self, event):
        if self.search_job:
            self.after_cancel(self.search_job)
        self.search_job = self.after(500, self.update_processes_threaded)

    def update_processes_threaded(self):
        threading.Thread(target=self.update_processes, daemon=True).start()

    def update_processes(self):
        search_term = self.search_var.get().lower()
        process_list = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                cpu = proc.info['cpu_percent']
                mem = proc.info['memory_percent']
                if search_term in name.lower():
                    process_list.append((pid, name, round(cpu, 1), round(mem, 1)))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        process_list = sorted(process_list, key=lambda x: x[2], reverse=True)[:100]
        self.after(0, self.populate_tree, process_list)
        self.after(5000, self.update_processes_threaded)

    def populate_tree(self, process_list):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for proc in process_list:
            self.tree.insert("", "end", values=proc)

    def kill_selected_process(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a process to terminate.")
            return

        pid = int(self.tree.item(selected[0], 'values')[0])
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            confirm = messagebox.askyesno("Confirm Kill", f"Are you sure you want to terminate '{name}' (PID: {pid})?")
            if confirm:
                proc.terminate()
                proc.wait(timeout=3)
                messagebox.showinfo("Terminated", f"'{name}' (PID: {pid}) has been terminated.")
                self.update_processes_threaded()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
            messagebox.showerror("Error", f"Failed to terminate process: {e}")

class SMTDApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Monitoring and Threat Detection Tool - SMTD")
        self.geometry("950x600")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        graph_frame = LiveGraphFrame(notebook)
        process_frame = ProcessViewerFrame(notebook)

        notebook.add(graph_frame, text="Live Monitoring")
        notebook.add(process_frame, text="Process Viewer")

if __name__ == '__main__':
    app = SMTDApp()
    app.mainloop()