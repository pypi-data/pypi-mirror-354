<script lang="ts">
  import { onMount } from "svelte";

  // Required and commonly injected by Gradio
  export let label;
  export let visible;
  export let elem_id;
  export let elem_classes;
  export let theme_mode;

  // Optional injected metadata (suppress warnings)
  export let target;
  export let interactive;
  export let server;
  export let gradio;
  export let root;

  export let value: Array<Record<string, any>> = [];
  export let rows_per_page: number = 10;
  // export let default_sort_column: string = "ID";
  // export let default_sort_direction: "asc" | "desc" = "asc";

  let currentPage: number = 1;
  let totalPages: number = 1;
  let view: Array<Record<string, any>> = [];

  let search_term: string = "";
  let filtered_value: Array<Record<string, any>> = [];

  let sort_column: string | null = null;
  let sort_direction: "asc" | "desc" | null = null;

  let selected_row_index: number | null = null;
  let selected_row_data: Record<string, any> | null = null;

  // This will hold the selected row
  let selectedRow = null;

  // Filter the value based on the search term
  $: filtered_value = value
    .filter((row) =>
      Object.values(row)
        .join(" ")
        .toLowerCase()
        .includes(search_term.toLowerCase()),
    )
    .slice()
    .sort((a, b) => {
      if (!sort_column || !sort_direction) return 0;

      let valA = a[sort_column];
      let valB = b[sort_column];

      // Handle nulls
      if (valA == null) valA = "";
      if (valB == null) valB = "";

      // Numeric comparison
      if (!isNaN(Number(valA)) && !isNaN(Number(valB))) {
        valA = Number(valA);
        valB = Number(valB);
        return sort_direction === "asc" ? valA - valB : valB - valA;
      }

      // String comparison
      valA = String(valA);
      valB = String(valB);
      return sort_direction === "asc"
        ? valA.localeCompare(valB)
        : valB.localeCompare(valA);
    });

  function toggleSort(col: string) {
    if (sort_column !== col) {
      sort_column = col;
      sort_direction = "asc";
    } else if (sort_direction === "asc") {
      sort_direction = "desc";
    } else if (sort_direction === "desc") {
      sort_column = null;
      sort_direction = null;
    } else {
      sort_direction = "asc";
    }

    currentPage = 1;
  }

  // Update pagination view
  function paginate() {
    totalPages = Math.ceil(filtered_value.length / rows_per_page);
    currentPage = Math.min(Math.max(1, currentPage), totalPages || 1);
    const start = (currentPage - 1) * rows_per_page;
    view = filtered_value.slice(start, start + rows_per_page);
  }

  function onRowClick(index: number) {
    selected_row_index = index + (currentPage - 1) * rows_per_page;
    selected_row_data = filtered_value[selected_row_index];
    console.log("Row clicked:", selected_row_data);
  }

  function exportCurrentPageAsCSV() {
    if (view.length === 0) return;
    const rows = [Object.keys(view[0])].concat(view.map(row => Object.values(row)));
    downloadCSV(rows, `export_page_${currentPage}.csv`);
  }

  function exportEntireTableAsCSV() {
    if (filtered_value.length === 0) return;
    const rows = [Object.keys(filtered_value[0])].concat(filtered_value.map(row => Object.values(row)));
    downloadCSV(rows, "export_full_table.csv");
  }

  function downloadCSV(data: Array<any>, filename: string) {
    const csvContent = data.map(e => e.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  function goToPage(p: number) {
    currentPage = p;
    paginate();
  }

  function next() {
    goToPage(currentPage + 1);
  }

  function prev() {
    goToPage(currentPage - 1);
  }

  $: if (filtered_value && filtered_value.length >= 0) {
    paginate();
  }

  $: if (value.length > 0) {
    currentPage = 1; // Reset page when new data arrives
  }

  $: if (search_term !== "") {
    currentPage = 1;
  }

  // Reset Selection on Search or Page Change
  // $: if (search_term || currentPage) {
  //   selected_row_index = null;
  //   selected_row_data = null;
  // }

  // $: if (value.length === 0) {
  // 	console.warn("No data passed from Python!");
  // } else {
  // 	console.log("Data received:", value);
  // }
  // $: console.log("value updated", value);

  onMount(() => paginate());
</script>

<div class="toolbar">
  <div class="toolbar-left">
    <label>
      Rows per page:
      <select
        bind:value={rows_per_page}
        on:change={() => {
          currentPage = 1;
          paginate();
        }}
      >
        <option value={5}>5</option>
        <option value={10}>10</option>
        <option value={25}>25</option>
        <option value={50}>50</option>
      </select>
    </label>
  </div>

  <div class="toolbar-right">
    <input
      type="text"
      placeholder="Search..."
      bind:value={search_term}
      on:input={() => {
        currentPage = 1;
        paginate();
      }}
      class="search-box"
    />
  </div>
</div>

<div>
  <!-- 📊 Table Display -->
  <table>
    <thead>
      <tr>
        {#if view.length > 0}
          {#each Object.keys(view[0]) as col}
            <th on:click={() => toggleSort(col)} class="sortable">
              {col}
              {#if sort_column === col}
                {#if sort_direction === "asc"}
                  🔼
                {:else if sort_direction === "desc"}
                  🔽
                {/if}
              {/if}
            </th>
          {/each}
        {/if}
      </tr>
    </thead>
    <tbody>
      {#each view as row, index}
        <tr
          class:selected={selected_row_index ===
            index + (currentPage - 1) * rows_per_page}
          on:click={() => onRowClick(index)}
        >
          {#each Object.values(row) as cell}
            <td>{cell}</td>
          {/each}
        </tr>
      {/each}
      {#if view.length === 0}
        <tr>
          <td width="100%">No data found</td>
        </tr>
      {/if}
    </tbody>
  </table>

  <div class="controls">
    <button on:click={prev} disabled={currentPage === 1}>⬅️ Prev</button>
    <span>Page {currentPage} of {totalPages}</span>
    <button on:click={next} disabled={currentPage === totalPages}
      >Next ➡️</button
    >
  </div>
  <div class="export-controls">
    <button on:click={exportCurrentPageAsCSV}>📤 Export Current Page as CSV</button>
    <button on:click={exportEntireTableAsCSV}>📄 Export Entire Table as CSV</button>
  </div>
</div>

<style>
  .toolbar {
    display: flex;
    justify-content: space-between; /* 👈 Align children to ends */
    align-items: center;
    margin-bottom: 10px;
  }

  .toolbar-left select,
  .toolbar-right input.search-box {
    padding: 6px 10px;
    border: 1px solid #f97316;       /* orange-500 border */
    border-radius: 4px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .toolbar-left select {
    padding-right: 2.5rem;           /* 👈 reserve space for dropdown arrow */
  }

  .toolbar-left select:focus,
  .toolbar-right input.search-box:focus {
    border-color: #fb923c;           /* orange-400 on focus */
    box-shadow: 0 0 0 2px #fde68a;   /* optional soft glow */
  }

  .toolbar-left select:hover,
  .toolbar-right input.search-box:hover {
    background-color: #fff7ed;       /* orange-50 on hover */
  }

  label {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .search-box {
    padding: 5px;
    font-size: 14px;
    width: 200px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid #fcd34d; /* orange-300 */
  }

  th,
  td {
    padding: 6px 12px;
    border: 1px solid #fcd34d;
    text-align: left;
  }

  th.sortable {
    cursor: pointer;
    user-select: none;
    color: #c2410c; /* dark orange */
  }

  th.sortable:hover {
    background-color: #f0f0f0;
  }

  tr {
    cursor: pointer;
  }

  tr.selected {
    background-color: #fed7aa; /* orange-200 */
    font-weight: bold;
  }

  tr:hover {
    background-color: #fff7ed; /* orange-50 */
  }

  button:disabled {
    opacity: 0.5;
  }

  .controls, .export-controls {
    margin-top: 10px;
    display: flex;
    justify-content: center;
    gap: 12px;
    align-items: center;
  }

  .export-controls button,
  .controls button {
    padding: 6px 12px;
    font-size: 14px;
    background-color: white;
    color: #f97316;
    cursor: pointer;
    transition: background-color 0.2s, color 0.2s;
  }

  .export-controls button:hover,
  .controls button:hover {
    background-color: #f97316;
    color: white;
  }
</style>



<!-- <script lang="ts">
	import { JsonView } from "@zerodevx/svelte-json-view";

	import type { Gradio } from "@gradio/utils";
	import { Block, Info } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import type { SelectData } from "@gradio/utils";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = false;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let gradio: Gradio<{
		change: never;
		select: SelectData;
		input: never;
		clear_status: LoadingStatus;
	}>;
</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
			on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
		/>
	{/if}

	<JsonView json={value} />
</Block> -->
