import pandas as pd

def export_results(pages, memory_history, page_faults, filename="simulation_results.csv"):
    data = []
    memory_set = set()
    
    for i, page in enumerate(pages):
        state = memory_history[i]
        current_set = set(state)

        if i == 0 or page not in memory_history[i - 1]:
            status = "Page Fault"
        else:
            status = "Hit"

        row = {
            "Step": i + 1,
            "Page": page,
            "Memory State": str(state),
            "Status": status
        }
        data.append(row)

    df = pd.DataFrame(data)
    df.loc[len(df.index)] = {"Step": "Total Faults", "Page": "", "Memory State": "", "Status": page_faults}
    df.to_csv(filename, index=False)
