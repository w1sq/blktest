"""
Block device performance testing
"""

import os
import time
import json
import argparse
import subprocess

from pygnuplot import gnuplot


def run_fio_test(name: str, filename: str, iodepth: int, rw: str) -> dict:
    """Running fio test with given parameters"""
    fio_cmd = [
        "fio",
        f"--name={name}",
        f"--filename={filename}",
        "--ioengine=libaio",
        "--direct=1",
        "--bs=4k",
        "--size=1G",
        "--numjobs=1",
        f"--rw={rw}",
        f"--iodepth={iodepth}",
        "--output-format=json",
        "--time_based",
        "--runtime=30",
    ]

    result = subprocess.run(fio_cmd, capture_output=True, text=True, check=True)

    try:
        data = json.loads(result.stdout)["jobs"][0]
        if "read" in data:
            print(f"Read latency: {data['read']['clat_ns']['mean']/1000} μs")
        if "write" in data:
            print(f"Write latency: {data['write']['clat_ns']['mean']/1000} μs")
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"FIO output: {result.stdout}")
        raise


def create_plot(results: list[dict], output: str):
    """Create a plot of latency vs IO depth"""
    gp = gnuplot.Gnuplot()

    gp("set terminal png size 1600,900 enhanced")
    gp(f'set output "{output}"')

    read_data = {}
    write_data = {}

    for result in results:
        iodepth = result["iodepth"]
        if "read" in result and result["read"]["clat_ns"]["mean"] > 0:
            read_data[iodepth] = result["read"]["clat_ns"]["mean"] / 1000
        if "write" in result and result["write"]["clat_ns"]["mean"] > 0:
            write_data[iodepth] = result["write"]["clat_ns"]["mean"] / 1000

    temp_dir = os.getcwd()
    read_file = os.path.join(temp_dir, "read_data.tmp")
    write_file = os.path.join(temp_dir, "write_data.tmp")

    if read_data:
        with open(read_file, "w", encoding="utf-8") as f:
            for depth, lat in sorted(read_data.items()):
                f.write(f"{depth} {lat}\n")

    if write_data:
        with open(write_file, "w", encoding="utf-8") as f:
            for depth, lat in sorted(write_data.items()):
                f.write(f"{depth} {lat}\n")

    files_exist = all(
        os.path.exists(f) and os.path.getsize(f) > 0
        for f in [read_file, write_file]
        if read_data or write_data
    )

    if not files_exist:
        raise RuntimeError("Temporary data files were not created properly")

    gp("set logscale xy")
    gp("set grid xtics ytics mxtics mytics")
    gp('set grid lt 1 lc rgb "#808080" lw 1')
    gp('set xlabel "IO Depth"')
    gp('set ylabel "Latency (μs)"')
    gp('set title "Latency vs IO Depth\\nBlock Device Performance Test"')
    gp("set key left top")
    gp("set yrange [1:*]")
    gp("set xrange [0.8:300]")

    gp('set style line 1 lt 1 lc rgb "#0060ad" lw 2 pt 7 ps 1.5')
    gp('set style line 2 lt 1 lc rgb "#dd181f" lw 2 pt 5 ps 1.5')

    gp("set mxtics 10")
    gp("set mytics 10")

    plot_cmd = []
    if os.path.exists(read_file):
        plot_cmd.append(f"'{read_file}' with linespoints ls 1 title 'Read Latency'")
    if os.path.exists(write_file):
        plot_cmd.append(f"'{write_file}' with linespoints ls 2 title 'Write Latency'")

    if plot_cmd:
        plot_command = f"plot {', '.join(plot_cmd)}"
        gp(plot_command)
    else:
        print("No data files found for plotting!")

    gp.close()
    time.sleep(0.1)

    for file in [read_file, write_file]:
        if os.path.exists(file):
            try:
                os.remove(file)
            except OSError as e:
                print(f"Warning: Could not remove temporary file {file}: {e}")


def main():
    """Running block device performance testing"""
    parser = argparse.ArgumentParser(description="Block device performance testing")
    parser.add_argument("--name", required=True, help="Test name")
    parser.add_argument("--filename", required=True, help="Device or file to test")
    parser.add_argument("--output", required=True, help="Output PNG file path")

    args = parser.parse_args()

    iodepths = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    results = []

    for rw in ["randread", "randwrite"]:
        for depth in iodepths:
            print(f"\nRunning test with iodepth={depth}, rw={rw}")
            try:
                result = run_fio_test(args.name, args.filename, depth, rw)
                result["iodepth"] = depth
                results.append(result)
            except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
                print(f"Error running test: {e}")

    create_plot(results, args.output)


if __name__ == "__main__":
    main()
