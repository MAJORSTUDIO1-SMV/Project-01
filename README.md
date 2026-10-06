## Project Overview
This project provides an interactive visual analysis of the Cooper Hewitt Smithsonian Design Museum's collection using the museum's API. By standardizing thousands of extracted hexadecimal colors into CSS3 color families, the prototype allows users to explore chromatic trends across 93,010 museum objects.

The interface features two complementary exploratory views:
1. **Treemap View (Macro Collection):** Visualizes the relative volume of representative colors across the entire collection.
2. **Top 12 Categories View (Category Stacks):** Displays stacked 100% normalized bars for the top 12 object categories, aligning colors globally by hue family to enable comparative cross-category palette analysis.

## Visual Design Choices & Justifications

* **Composition & Layout:** A dual-view architecture was chosen to provide both macro-level exploration (Treemap) and category-level comparative analysis (Stacked Bars).
* **Color & Alignment:** Colors were categorized into standard CSS3 families. In the stacked view, blocks follow a fixed global alignment by hue order to ensure horizontal visual continuity.
* **Typography & Hierarchy:** Bold display typefaces (`Impact`) were used for primary headings, paired with clean sans-serif typography (`Arial`) for data labels and tooltips to maximize legibility.
* **Dark UI & Contrast:** A high-contrast dark background (`#0f1115`) was selected to minimize visual glare and ensure the color palettes stand out vibrantly.

## Screenshots

![Treemap View](images/tree_map1.png)
![Treemap View](images/tree_map2.png)

![Category Stacks View](images/stack1.png)
![Category Stacks View](images/stack2.png)

![Category Textile View](images/textile1.png)
![Category Textile View](images/textile2.png)

