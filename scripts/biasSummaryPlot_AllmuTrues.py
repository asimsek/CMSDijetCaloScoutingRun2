import subprocess

def run_bias_summary_plot(year, cfg_file1, cfg_file2, mu_true, signal):
    cmd = [
        "python",
        "biasSummaryPlot.py",
        "--year", year,
        "--cfgFile1", cfg_file1,
        "--cfgFile2", cfg_file2,
        "--muTrue", str(mu_true),
        "--signal", signal
    ]
    subprocess.run(cmd)

def main():
    year = "2018D"
    cfg_files = ["dijet_Atlas", "dijetSep"]
    mu_true_values = [0, 1, 2]
    signals = ["gg", "qg", "qq"]

    for mu_true in mu_true_values:
        for signal in signals:
            for i, cfg_file1 in enumerate(cfg_files):
                run_bias_summary_plot(year, cfg_file1, cfg_files[1], mu_true, signal)

if __name__ == "__main__":
    main()

