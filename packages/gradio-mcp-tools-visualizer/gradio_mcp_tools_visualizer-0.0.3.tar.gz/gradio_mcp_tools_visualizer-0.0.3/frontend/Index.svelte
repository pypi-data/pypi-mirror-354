<script lang="ts">
    import { Block, Info } from "@gradio/atoms";
    import { StatusTracker } from "@gradio/statustracker";
    import type { LoadingStatus } from "@gradio/statustracker";
    import type { Gradio } from "@gradio/utils";

    export let elem_id = "";
    export let elem_classes: string[] = [];
    export let visible = true;
    export let value: any = {
        tool_summaries: []
    };
    export let container = true;
    export let scale: number | null = null;
    export let min_width: number | undefined = undefined;
    export let loading_status: LoadingStatus;
    export let gradio: Gradio<{
        change: never;
        select: never;
        input: any;
        clear_status: LoadingStatus;
    }>;

    let searchQuery = "";
    let selectedTool = null;

    $: filteredTools = value.tool_summaries.filter((tool) => 
        tool.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width} style="padding: 2rem; background: #f9fafb; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    {#if loading_status}
        <StatusTracker
            autoscroll={gradio.autoscroll}
            i18n={gradio.i18n}
            {...loading_status}
            on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
        />
    {/if}

    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1 style="font-size: 1.5rem;">🚀 MCP Tools Visualizer</h1>
    </div>

    <div style="display: flex; margin-top: 1rem; gap: 2rem;">
        <div style="flex: 1;">
            <h3 style="margin-bottom: 1rem;">Tools</h3>
            <input 
                type="text"
                placeholder="🔍 Search Tools..."
                bind:value={searchQuery}
                style="padding: 0.5rem; width: 100%; border-radius: 4px; border: 1px solid #ccc; margin-bottom: 1rem;"
            />

            {#each filteredTools as tool}
                <button
                    style="padding: 0.5rem; width: 100%; text-align: left; border: none; background-color: transparent; cursor: pointer;"
                    on:click={() => selectedTool = tool}
                >
                    {tool.name}
                </button>
            {/each}
        </div>

        <div style="flex: 2;">
            {#if selectedTool}
                <h2>🛠️ Tool: {selectedTool.name}</h2>
                <h4 style="margin-top: 2rem;">Example Inputs:</h4>
                <pre style="padding:0.75rem; border-radius: 4px;">{JSON.stringify(selectedTool.inputs, null, 2)}</pre>
            {/if}
        </div>
    </div>
</Block>