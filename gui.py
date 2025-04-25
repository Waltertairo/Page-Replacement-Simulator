import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from algorithms import fifo, lru, opt
from analysis import export_results
from tkinter import filedialog
from utils import generate_random_reference

def start_gui():
    window = tk.Tk()
    window.title("Page Replacement Simulator")
    window.geometry("600x400")
    window.configure(bg="#121212")  # Dark background

    style = ttk.Style()
    style.theme_use("default")

    # Custom styling
    style.configure("TLabel", background="#121212", foreground="#D7BFFF", font=("Segoe UI", 10))
    style.configure("TButton", background="#5E17EB", foreground="white", font=("Segoe UI", 10, "bold"))
    style.configure("TEntry", fieldbackground="#1E1E1E", foreground="white", borderwidth=2)
    style.configure("TCombobox",
                    fieldbackground="#1E1E1E",
                    background="#1E1E1E",
                    foreground="white",
                    selectbackground="#1E1E1E",
                    selectforeground="white")
    style.map("TCombobox",
              fieldbackground=[("readonly", "#1E1E1E")],
              background=[("readonly", "#1E1E1E")],
              foreground=[("readonly", "white")])

    ttk.Label(window, text="PAGE REPLACEMENT SIMULATOR", font=("Segoe UI", 18, "bold")).pack(pady=8, padx=20)

    input_frame = tk.Frame(window, bg="#1E1E1E", bd=2, relief="ridge")
    input_frame.pack(pady=15)

    frame_input = tk.IntVar()
    ref_string_input = tk.StringVar()
    algo_choice = tk.StringVar(value="FIFO")

    tk.Label(input_frame, text="Number of Frames:", bg="#1E1E1E", fg="#D7BFFF", font=("Segoe UI", 10)).pack(pady=8, padx=20)
    ttk.Entry(input_frame, textvariable=frame_input).pack(pady=5, padx=20)

    tk.Label(input_frame, text="Page Reference String (e.g., 7 0 1 2 0 3 0 4):", bg="#1E1E1E", fg="#D7BFFF", font=("Segoe UI", 10)).pack(pady=8, padx=20)
    ttk.Entry(input_frame, textvariable=ref_string_input).pack(pady=5, padx=20)

    tk.Label(input_frame, text="Select Algorithm:", bg="#1E1E1E", fg="#D7BFFF", font=("Segoe UI", 10)).pack(pady=8, padx=20)
    algo_menu = ttk.Combobox(input_frame, textvariable=algo_choice,
                             values=["FIFO", "LRU", "OPT"], state="readonly")
    algo_menu.pack(pady=5, padx=20)

    def clear_inputs():
        frame_input.set(0)
        ref_string_input.set("")
        algo_choice.set("FIFO")

    def generate_random():
        random_str = generate_random_reference()
        ref_string_input.set(random_str)

    ttk.Button(input_frame, text="Generate Random", command=generate_random).pack(pady=5)

    def run_simulation():
        try:
            frames = frame_input.get()
            pages = list(map(int, ref_string_input.get().split()))
            algo = algo_choice.get()

            if algo == "FIFO":
                faults, history = fifo(pages, frames)
            elif algo == "LRU":
                faults, history = lru(pages, frames)
            elif algo == "OPT":
                faults, history = opt(pages, frames)

            result_window = tk.Toplevel(window)
            result_window.title("Simulation Result")
            result_window.configure(bg="white")

            tk.Label(result_window, text=f"Page Faults: {faults}", font=("Segoe UI", 12, "bold"), bg="white", fg="black").pack(pady=10)

            for i, frame in enumerate(history):
                status = "Page Fault" if i == 0 or pages[i] not in history[i - 1] else "Hit"
                tk.Label(result_window, text=f"Step {i+1}: {frame} → {status}", font=("Segoe UI", 10), bg="white", fg="black").pack()

            def export():
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv")],
                    title="Save simulation result as"
                )
                if file_path:
                    export_results(pages, history, faults, filename=file_path)
                    messagebox.showinfo("Exported", f"Results saved to:\n{file_path}")

            ttk.Button(result_window, text="Export to CSV", command=export).pack(pady=10)

        except Exception as e:
            tk.messagebox.showerror("Error", f"Invalid input: {e}")

    def show_comparison_graph():
        try:
            frames = frame_input.get()
            pages = list(map(int, ref_string_input.get().split()))

            fifo_faults, _ = fifo(pages, frames)
            lru_faults, _ = lru(pages, frames)
            opt_faults, _ = opt(pages, frames)

            algos = ['FIFO', 'LRU', 'OPT']
            faults = [fifo_faults, lru_faults, opt_faults]

            plt.figure(figsize=(6, 4))
            plt.bar(algos, faults)
            plt.title('Page Faults Comparison')
            plt.xlabel('Algorithm')
            plt.ylabel('Page Faults')
            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    ttk.Button(window, text="Run Simulation", command=run_simulation).pack(pady=10, padx=20)
    ttk.Button(window, text="Compare All Algorithms", command=show_comparison_graph).pack(pady=10, padx=20)
    ttk.Button(window, text="Clear All", command=clear_inputs).pack(pady=10, padx=20)

    window.mainloop()