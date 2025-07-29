"""System resource monitoring for ML workloads"""
import psutil
import threading
import time
from typing import Dict, Any, Optional, Callable
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich import box
import os

# Try to import GPU monitoring if available
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

class SystemMonitor:
    """Monitors system resources and provides real-time stats"""
    
    def __init__(self, refresh_interval: float = 2.0):
        """Initialize the system monitor
        
        Args:
            refresh_interval: How often to update stats (in seconds)
        """
        self.refresh_interval = refresh_interval
        self.stop_event = threading.Event()
        self.monitoring_thread = None
        self.stats = {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "gpu_percent": 0.0,
            "gpu_memory_percent": 0.0,
            "gpu_name": "N/A",
            "disk_percent": 0.0
        }
        self.callbacks = []
    
    def start(self):
        """Start monitoring system resources in the background"""
        if self.monitoring_thread is None or not self.monitoring_thread.is_alive():
            self.stop_event.clear()
            self.monitoring_thread = threading.Thread(target=self._monitor_resources, daemon=True)
            self.monitoring_thread.start()
    
    def stop(self):
        """Stop the monitoring thread"""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.stop_event.set()
            self.monitoring_thread.join(timeout=1.0)
    
    def add_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Add a callback to be invoked when stats are updated
        
        Args:
            callback: Function that takes the stats dict as parameter
        """
        self.callbacks.append(callback)
    
    def _monitor_resources(self):
        """Background thread that monitors system resources"""
        while not self.stop_event.is_set():
            # Update CPU usage
            self.stats["cpu_percent"] = psutil.cpu_percent(interval=None)
            
            # Update memory usage
            memory = psutil.virtual_memory()
            self.stats["memory_percent"] = memory.percent
            
            # Update disk usage
            disk = psutil.disk_usage('/')
            self.stats["disk_percent"] = disk.percent
            
            # Update GPU usage if available
            if GPU_AVAILABLE:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        gpu = gpus[0]  # Use first GPU
                        self.stats["gpu_percent"] = gpu.load * 100
                        self.stats["gpu_memory_percent"] = gpu.memoryUtil * 100
                        self.stats["gpu_name"] = gpu.name
                except:
                    pass
            
            # Call any registered callbacks
            for callback in self.callbacks:
                try:
                    callback(self.stats)
                except:
                    pass
                    
            time.sleep(self.refresh_interval)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get the current resource statistics
        
        Returns:
            Dict containing system resource stats
        """
        return self.stats.copy()

class SystemMonitorDisplay:
    """UI component to display system resource usage"""
    
    def __init__(self, console: Console, monitor: SystemMonitor, compact: bool = False):
        """Initialize the system monitor display
        
        Args:
            console: Rich Console to use for display
            monitor: SystemMonitor instance to get stats from
            compact: Whether to use compact display format
        """
        self.console = console
        self.monitor = monitor
        self.compact = compact
        
        # Register callback to update display when stats change
        self.monitor.add_callback(self.update_stats)
        self.stats = self.monitor.get_stats()
    
    def update_stats(self, stats: Dict[str, Any]) -> None:
        """Update the current stats
        
        Args:
            stats: New system stats to display
        """
        self.stats = stats
    
    def get_display(self) -> Panel:
        """Get a Rich Panel containing the system resource display
        
        Returns:
            Panel with resource utilization
        """
        if self.compact:
            return self._get_compact_display()
        else:
            return self._get_full_display()
    
    def _get_compact_display(self) -> Panel:
        """Get a compact version of the resource display
        
        Returns:
            Panel with compact resource utilization info
        """
        # Create compact display with just numbers
        stats = self.stats
        
        text = (
            f"CPU: [{'green' if stats['cpu_percent'] < 70 else 'yellow' if stats['cpu_percent'] < 90 else 'red'}]"
            f"{stats['cpu_percent']:.0f}%[/] | "
            f"RAM: [{'green' if stats['memory_percent'] < 70 else 'yellow' if stats['memory_percent'] < 90 else 'red'}]"
            f"{stats['memory_percent']:.0f}%[/]"
        )
        
        if GPU_AVAILABLE and stats['gpu_name'] != "N/A":
            text += (
                f" | GPU: [{'green' if stats['gpu_percent'] < 70 else 'yellow' if stats['gpu_percent'] < 90 else 'red'}]"
                f"{stats['gpu_percent']:.0f}%[/] | "
                f"VRAM: [{'green' if stats['gpu_memory_percent'] < 70 else 'yellow' if stats['gpu_memory_percent'] < 90 else 'red'}]"
                f"{stats['gpu_memory_percent']:.0f}%[/]"
            )
        
        return Panel(text, title="[bold]Resources[/]", border_style="dim", box=box.ROUNDED, width=None, padding=(0, 1))
    
    def _get_full_display(self) -> Panel:
        """Get a detailed version of the resource display
        
        Returns:
            Panel with detailed resource utilization info
        """
        # Create a table to display resource usage
        table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        table.add_column("Resource", style="dim")
        table.add_column("Usage")
        
        # Add CPU usage
        cpu_color = "green" if self.stats["cpu_percent"] < 70 else "yellow" if self.stats["cpu_percent"] < 90 else "red"
        table.add_row("CPU:", f"[{cpu_color}]{self.stats['cpu_percent']:.1f}%[/]")
        
        # Add memory usage
        mem_color = "green" if self.stats["memory_percent"] < 70 else "yellow" if self.stats["memory_percent"] < 90 else "red"
        table.add_row("Memory:", f"[{mem_color}]{self.stats['memory_percent']:.1f}%[/]")
        
        # Add GPU usage if available
        if GPU_AVAILABLE and self.stats['gpu_name'] != "N/A":
            table.add_row("GPU:", f"[dim]{self.stats['gpu_name']}[/]")
            
            gpu_color = "green" if self.stats["gpu_percent"] < 70 else "yellow" if self.stats["gpu_percent"] < 90 else "red"
            table.add_row("GPU Usage:", f"[{gpu_color}]{self.stats['gpu_percent']:.1f}%[/]")
            
            vram_color = "green" if self.stats["gpu_memory_percent"] < 70 else "yellow" if self.stats["gpu_memory_percent"] < 90 else "red"
            table.add_row("GPU Memory:", f"[{vram_color}]{self.stats['gpu_memory_percent']:.1f}%[/]")
        
        # Add disk usage
        disk_color = "green" if self.stats["disk_percent"] < 70 else "yellow" if self.stats["disk_percent"] < 90 else "red"
        table.add_row("Disk:", f"[{disk_color}]{self.stats['disk_percent']:.1f}%[/]")
        
        return Panel(table, title="[bold]System Resources[/]", border_style="dim", box=box.ROUNDED)

def setup_system_monitor(console: Console, refresh_interval: float = 2.0, compact: bool = True) -> SystemMonitorDisplay:
    """Setup and start the system monitor
    
    Args:
        console: Rich console to use for display
        refresh_interval: How often to refresh stats (in seconds)
        compact: Whether to use compact display format
        
    Returns:
        SystemMonitorDisplay object ready to use
    """
    monitor = SystemMonitor(refresh_interval=refresh_interval)
    display = SystemMonitorDisplay(console, monitor, compact=compact)
    monitor.start()
    return display
