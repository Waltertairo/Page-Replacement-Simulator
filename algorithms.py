def fifo(pages, frames):
    memory = []
    page_faults = 0
    history = []

    for page in pages:
        if page not in memory:
            page_faults += 1
            if len(memory) == frames:
                memory.pop(0)
            memory.append(page)
        history.append(memory.copy())

    return page_faults, history


def lru(pages, frames):
    memory = []
    page_faults = 0
    recently_used = []
    history = []

    for page in pages:
        if page not in memory:
            page_faults += 1
            if len(memory) == frames:
                lru_page = recently_used.pop(0)
                memory.remove(lru_page)
            memory.append(page)
        else:
            recently_used.remove(page)  # Update recency

        # ✅ Important: Only add to memory if it’s a miss
        if page not in memory:
            memory.append(page)

        recently_used.append(page)
        history.append(memory.copy())

    return page_faults, history



def opt(pages, frames):
    memory = []
    page_faults = 0
    history = []

    for i in range(len(pages)):
        page = pages[i]
        if page not in memory:
            page_faults += 1
            if len(memory) < frames:
                memory.append(page)
            else:
                future = pages[i+1:]
                indexes = []
                for mem_page in memory:
                    if mem_page in future:
                        indexes.append(future.index(mem_page))
                    else:
                        indexes.append(float('inf'))
                to_replace = indexes.index(max(indexes))
                memory[to_replace] = page
        history.append(memory.copy())

    return page_faults, history
