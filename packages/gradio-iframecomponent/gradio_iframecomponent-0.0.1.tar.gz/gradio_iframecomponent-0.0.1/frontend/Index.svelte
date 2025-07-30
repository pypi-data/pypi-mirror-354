<script lang="ts">
    import { Block } from "@gradio/atoms";
    import { StatusTracker } from "@gradio/statustracker";
    import type { Gradio, SelectData } from "@gradio/utils";

    export let gradio: Gradio<{
        change: string;
        input: string;
        select: SelectData;
    }>;
    
    export let elem_id = "";
    export let elem_classes: string[] = [];
    export let visible = true;
    export let value = "";
    export let loading_status: any;
    export let label: string;
    export let show_label: boolean;
    export let interactive: boolean;
    export let root: string;

    let iframe_container: HTMLDivElement;
    
    // Handle iframe load events for dynamic sizing
    function handleIframeLoad(event: Event) {
        const iframe = event.target as HTMLIFrameElement;
        try {
            // Attempt to adjust height based on content (same-origin only)
            if (iframe.contentDocument) {
                const contentHeight = iframe.contentDocument.body.scrollHeight;
                iframe.style.height = contentHeight + "px";
            }
        } catch (e) {
            // Cross-origin iframes will throw security errors - this is expected
            console.log("Cannot access iframe content (cross-origin)");
        }
    }

    // Update value when content changes
    function updateValue(newValue: string) {
        value = newValue;
        gradio.dispatch("change", value);
        gradio.dispatch("input", value);
    }

    $: if (iframe_container && value) {
        iframe_container.innerHTML = value;
        
        // Add load event listeners to all iframes
        const iframes = iframe_container.querySelectorAll('iframe');
        iframes.forEach(iframe => {
            iframe.addEventListener('load', handleIframeLoad);
        });
    }
</script>

<Block {visible} {elem_id} {elem_classes} allow_overflow={false} padding={false}>
    {#if loading_status}
        <StatusTracker autoscroll={gradio.autoscroll} i18n={gradio.i18n} {...loading_status} />
    {/if}
    
    {#if show_label}
        <label for="iframe-{elem_id}" class="block text-sm font-medium text-gray-700 mb-2">
            {label}
        </label>
    {/if}
    
    <div 
        bind:this={iframe_container}
        class="iframe-container w-full"
        style="min-height: 300px; border-radius: 8px; overflow: hidden;"
    />
    
    {#if interactive}
        <div class="mt-2">
            <input
                type="url"
                placeholder="Enter URL or HTML content"
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
                on:input={(e) => updateValue(e.target.value)}
                value={value}
            />
        </div>
    {/if}
</Block>

<style>
    .iframe-container :global(iframe) {
        width: 100%;
        border: none;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .iframe-container :global(iframe):focus {
        outline: 2px solid #3b82f6;
        outline-offset: 2px;
    }
</style>
