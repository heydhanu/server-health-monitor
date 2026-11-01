import csv, os, datetime
import psutil
import matplotlib.pyplot as plt

CPU_LIMIT = 80
MEM_LIMIT = 85
DISK_LIMIT = 90
INTERVAL = 2
SAMPLES = 30

root = os.path.abspath(os.sep)
times, cpus, mems = [], [], []

with open("health_log.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["time", "cpu", "memory", "disk", "alerts"])
    for _ in range(SAMPLES):
        cpu = psutil.cpu_percent(interval=INTERVAL)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage(root).percent
        alerts = []
        if cpu > CPU_LIMIT:
            alerts.append("HIGH CPU")
        if mem > MEM_LIMIT:
            alerts.append("HIGH MEMORY")
        if disk > DISK_LIMIT:
            alerts.append("LOW DISK SPACE")
        t = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{t} CPU {cpu}% | MEM {mem}% | DISK {disk}% {'ALERT: ' + ', '.join(alerts) if alerts else ''}")
        w.writerow([t, cpu, mem, disk, ";".join(alerts)])
        times.append(t); cpus.append(cpu); mems.append(mem)

plt.figure(figsize=(10, 4))
plt.plot(times, cpus, label="CPU %")
plt.plot(times, mems, label="Memory %")
plt.axhline(CPU_LIMIT, color="red", linestyle="--", label="CPU limit")
plt.xticks(times[::5])
plt.title("Server Health Over Time")
plt.legend()
plt.tight_layout()
plt.savefig("health_chart.png", dpi=150)
print("Saved health_chart.png")
