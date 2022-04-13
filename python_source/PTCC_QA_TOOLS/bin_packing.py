def best_fit(areas, capacity):
    panels = [capacity] * len(areas)
    for area in areas:
        min_cap = capacity
        bi = 0
        for j, panel_cap in enumerate(panels):
            if panel_cap >= area and panel_cap - area < min_cap:
                bi = j
                min_cap = panel_cap - area
        if min_cap == capacity:
            panels.append(capacity - area)
        else:
            panels[bi] -= area
    return len([panel for panel in panels if panel != capacity])


def main():
    areas = [2, 5, 4, 7, 1, 3, 8]
    areas.sort(reverse=True)  # 8, 7, 5, 4, 3, 2, 1
    capacity = 10
    num_panels = best_fit(areas, capacity)
    print("Number of panels required: {}".format(num_panels))


if __name__ == "__main__":
    main()
