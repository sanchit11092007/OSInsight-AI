from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
import pandas as pd

from analytics.engine import AnalyticsEngine
from monitoring.data_logger import DataLogger
from monitoring.system_monitor import SystemMonitor
from utils.reporting import export_csv, export_pdf


class Dashboard(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("OSInsight-AI")
        self.geometry("1000x700")
        self.monitor, self.engine = SystemMonitor(), AnalyticsEngine()
        self.history = pd.DataFrame(columns=["timestamp", "cpu_percent", "memory_percent", "memory_used_mb", "disk_percent", "disk_used_gb", "process_count"])
        self.logger = DataLogger(Path("data") / "monitoring_history.csv")
        ctk.set_appearance_mode("dark")
        self._build()
        self.refresh()

    def _build(self) -> None:
        ctk.CTkLabel(self, text="OSInsight-AI", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=(20, 4))
        self.status = ctk.CTkLabel(self, text="Collecting system telemetry...")
        self.status.pack(pady=(0, 15))
        self.metrics = ctk.CTkFrame(self)
        self.metrics.pack(fill="x", padx=25, pady=8)
        self.metric_labels = {}
        for name in ("CPU", "Memory", "Disk", "Health"):
            label = ctk.CTkLabel(self.metrics, text=f"{name}\n--", width=190, height=85, font=ctk.CTkFont(size=18, weight="bold"))
            label.pack(side="left", expand=True, padx=8, pady=12)
            self.metric_labels[name] = label
        ctk.CTkLabel(self, text="Top Processes", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=28, pady=(18, 4))
        self.processes = tk.Text(self, height=17, bg="#1f2937", fg="white", relief="flat")
        self.processes.pack(fill="both", expand=True, padx=28, pady=4)
        controls = ctk.CTkFrame(self)
        controls.pack(fill="x", padx=25, pady=15)
        ctk.CTkButton(controls, text="Refresh", command=self.refresh).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(controls, text="Export CSV", command=self.save_csv).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(controls, text="Export PDF", command=self.save_pdf).pack(side="left", padx=10, pady=10)

    def refresh(self) -> None:
        snapshot = self.monitor.sample()
        self.logger.append(snapshot)
        self.history = pd.concat([self.history, pd.DataFrame([{k: v for k, v in snapshot.to_dict().items() if k != "top_processes"}])], ignore_index=True).tail(500)
        result = self.engine.analyze(self.history)
        self.metric_labels["CPU"].configure(text=f"CPU\n{snapshot.cpu_percent:.1f}%")
        self.metric_labels["Memory"].configure(text=f"Memory\n{snapshot.memory_percent:.1f}%")
        self.metric_labels["Disk"].configure(text=f"Disk\n{snapshot.disk_percent:.1f}%")
        self.metric_labels["Health"].configure(text=f"Health\n{result.health_score}/100")
        self.status.configure(text=f"{result.status}: CPU forecast {result.cpu_forecast:.1f}% | Memory forecast {result.memory_forecast:.1f}%")
        self.processes.delete("1.0", "end")
        for proc in snapshot.top_processes:
            self.processes.insert("end", f"{proc['name'][:32]:32} PID {proc['pid']:>6}   CPU {proc['cpu_percent']:>5.1f}%   MEM {proc['memory_percent']:>5.1f}%\n")
        self._result = result
        self.after(3000, self.refresh)

    def save_csv(self) -> None:
        path = export_csv(self.history, Path("reports") / "monitoring_export.csv")
        messagebox.showinfo("Export complete", f"Saved {path}")

    def save_pdf(self) -> None:
        path = export_pdf(self._result, Path("reports") / "system_health_report.pdf")
        messagebox.showinfo("Export complete", f"Saved {path}")
