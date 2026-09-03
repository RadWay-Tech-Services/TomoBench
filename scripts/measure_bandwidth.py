import numpy as np
import cupy as cp
import time


def measure_bandwidth(size_mb=1024, iterations=100):
    """
    Measures effective transfer bandwidth between CPU and GPU memory.

    Args:
        size_mb: The size of the data buffer in Megabytes (default 1024).
        iterations: Number of transfer operations to average.
    """

    # Configuration
    # Using float32 (4 bytes per element)
    size_bytes = size_mb * 1024 * 1024
    n_elements = size_bytes // 4

    print(f"[INFO] Generating {size_mb} MB of random data on Host...")
    # 1. Create Host Data
    host_data = np.random.rand(n_elements).astype(np.float32)

    # 2. Warmup (ensure CUDA context is ready)
    print("[INFO] Running warmup...")
    cp.zeros(1)

    # --- HOST TO DEVICE (H2D) ---
    print(f"[INFO] Measuring Host-to-Device transfer...")
    h2d_times = []
    for _ in range(iterations):
        start = time.perf_counter()
        # cp.array copies host memory to device memory (Synchronous)
        device_data = cp.array(host_data, blocking=True)
        end = time.perf_counter()
        h2d_times.append(end - start)

    avg_h2d = np.mean(h2d_times)
    h2d_bw = size_mb / avg_h2d  # MB/s

    # --- DEVICE TO HOST (D2H) ---
    print(f"[INFO] Measuring Device-to-Host transfer...")
    d2h_times = []
    for _ in range(iterations):
        start = time.perf_counter()
        # .get() copies device memory back to host (Synchronous)
        _ = device_data.get()
        end = time.perf_counter()
        d2h_times.append(end - start)

    avg_d2h = np.mean(d2h_times)
    d2h_bw = size_mb / avg_d2h  # MB/s

    # --- RESULTS ---
    print("\n" + "=" * 30)
    print(f"Data Size:       {size_mb} MB")
    print(f"Iterations:      {iterations}")
    print("-" * 30)
    print(f"H2D Avg Time:    {avg_h2d*1000:.2f} ms")
    print(f"H2D Bandwidth:   {h2d_bw:.2f} MB/s")
    print("-" * 30)
    print(f"D2H Avg Time:    {avg_d2h*1000:.2f} ms")
    print(f"D2H Bandwidth:   {d2h_bw:.2f} MB/s")
    print("=" * 30)


if __name__ == "__main__":
    # Run with 1GB buffer
    measure_bandwidth(size_mb=8 * 1024, iterations=5)
