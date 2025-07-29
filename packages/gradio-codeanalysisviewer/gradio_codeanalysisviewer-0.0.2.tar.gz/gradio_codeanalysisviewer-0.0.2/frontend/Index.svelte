<svelte:options accessors={true} />

<script lang="ts">
    import type { Gradio } from "@gradio/utils";
    import type { LoadingStatus } from "@gradio/statustracker";
    import { diffChars } from 'diff';
    import { marked } from 'marked';
    
    // Configure marked options for safe and proper rendering
    marked.setOptions({
        breaks: true,  // Convert line breaks to <br>
        gfm: true      // Use GitHub Flavored Markdown
    });

    // Define the expected structure of the 'value' prop based on OutputSchema
    interface OutputSchema {
        code: string;
        issue: string;
        reason: string;
        fixed_code?: string | null;
        feedback: string;
    }

    export let gradio: Gradio<{
        change: OutputSchema; // The component will dispatch the full object on change
        clear_status: LoadingStatus;
    }>;

    export let label = "Code Analysis";
    export let elem_id = "";
    export let elem_classes: string[] = [];
    export let visible = true;
    export let value: OutputSchema | null = null; // This is the main data prop
    export let show_label: boolean = true;
    export let scale: number | null = null;
    export let min_width: number | undefined = undefined;
    export let loading_status: LoadingStatus | undefined = undefined;
    // interactive property removed as unused

    // Reactive statement to dispatch change when value updates
    $: if (value) {
        gradio.dispatch("change", value);
    }

    // Default empty state or placeholder if value is null
    const default_value: OutputSchema = {
        code: "// No code provided",
        issue: "No issues to display.",
        reason: "N/A",
        fixed_code: null,
        feedback: "No feedback available."
    };

    $: display_value = value || default_value;

    // Reactive declaration for code diff
    let codeDiff = [];
    $: {
        if (display_value && display_value.code && display_value.fixed_code) {
            codeDiff = diffChars(display_value.code, display_value.fixed_code);
        } else {
            codeDiff = [];
        }
    }

</script>

<div 
    class="gradio-container"
    class:hidden={!visible}
    id={elem_id || null}
    class:block={elem_classes.includes('block')}
    style="width: {scale || 'auto'}; min-width: {min_width}px"
>
    {#if loading_status}
        <!-- StatusTracker component removed due to compatibility issues with Gradio 5.x -->
        <div class="status-message" class:error={loading_status.status === "error"}>  
            {loading_status.status === "pending" ? "Loading..." : loading_status.message || ""}
        </div>
    {/if}

    <div class="code-analysis-viewer">
        {#if show_label}
            <div class="gradio-label">{label}</div>
        {/if}

        {#if display_value}
            <div class="analysis-section">
                <h4>Original Code:</h4>
                <pre><code>{display_value.code}</code></pre>
            </div>

            <div class="analysis-section">
                <h4>Issue:</h4>
                <p>{display_value.issue}</p>
            </div>

            <div class="analysis-section">
                <h4>Reason:</h4>
                <p>{display_value.reason}</p>
            </div>

            {#if display_value.fixed_code}
                <div class="analysis-section">
                    <h4>Suggested Fix (Diff):</h4>
                    <pre class="diff-view">{#each codeDiff as part}<!--
                        --><span class="diff-part {part.added ? 'added' : (part.removed ? 'removed' : 'common')}">{part.value}</span><!--
                    -->{/each}</pre>
                </div>
            {/if}

            <div class="feedback-section">
                <h3>Feedback</h3>
                <div class="markdown-content">
                    {@html marked.parse(display_value.feedback || '')}
                </div>
            </div>
        {:else}
            <p>No analysis data to display.</p>
        {/if}
    </div>
</div>

<style>
    .code-analysis-viewer {
        font-family: var(--font-mono, monospace);
        font-size: var(--text-sm, 14px);
        color: var(--body-text-color, #333);
        border: 1px solid var(--border-color-primary, #e0e0e0);
        border-radius: var(--radius-lg, 8px);
        padding: var(--spacing-lg, 16px);
        background-color: var(--background-fill-primary, #f9f9f9);
    }

    .analysis-section {
        margin-bottom: var(--spacing-lg, 16px);
        padding-bottom: var(--spacing-md, 12px);
        border-bottom: 1px solid var(--border-color-secondary, #eee);
    }
    .analysis-section:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }

    .analysis-section h4 {
        font-weight: var(--font-weight-semibold, 600);
        color: var(--text-color-strong, #222);
        margin-top: 0;
        margin-bottom: var(--spacing-sm, 8px);
        font-size: var(--text-md, 16px);
    }

    pre {
        background-color: var(--background-fill-secondary, #f0f0f0);
        padding: var(--spacing-md, 12px);
        border-radius: var(--radius-md, 6px);
        overflow-x: auto;
        white-space: pre-wrap; 
        word-wrap: break-word; 
    }

    code {
        font-family: var(--font-mono, monospace);
    }

    p {
        line-height: 1.6;
        margin-top: 0;
        margin-bottom: 4px;
    }
    
    .feedback-section .markdown-content {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        line-height: 1.6;
        color: #333;
        overflow-wrap: break-word;
        word-break: break-word;
        max-width: 100%;
    }
    .feedback-section .markdown-content :global(p) {
        margin-bottom: 8px;
    }
    .feedback-section .markdown-content :global(ul),
    .feedback-section .markdown-content :global(ol) {
        padding-left: 20px;
        margin-bottom: 8px;
    }
    .feedback-section .markdown-content :global(li) {
        margin-bottom: 4px;
    }
    .feedback-section .markdown-content :global(code) {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        background-color: #e6f3ff;
        padding: 2px 4px;
        border-radius: 4px;
        font-size: 0.9em;
    }
    .feedback-section .markdown-content :global(pre) {
         background-color: #f0f0f0;
         padding: 12px;
         border-radius: 6px;
         overflow-x: auto;
         margin-bottom: 12px;
    }
    .feedback-section .markdown-content :global(pre code) {
        background-color: transparent;
        padding: 0;
        border-radius: 0;
    }
    
    /* Additional markdown styling */
    .feedback-section .markdown-content :global(h1),
    .feedback-section .markdown-content :global(h2),
    .feedback-section .markdown-content :global(h3),
    .feedback-section .markdown-content :global(h4),
    .feedback-section .markdown-content :global(h5),
    .feedback-section .markdown-content :global(h6) {
        margin-top: 16px;
        margin-bottom: 12px;
        font-weight: 600;
        line-height: 1.25;
        color: #111;
    }
    
    .feedback-section .markdown-content :global(h3) {
        font-size: 1.25rem;
    }
    
    .feedback-section .markdown-content :global(h4) {
        font-size: 1.1rem;
    }
    
    .feedback-section .markdown-content :global(a) {
        color: #3B82F6;
        text-decoration: none;
    }
    
    .feedback-section .markdown-content :global(a:hover) {
        text-decoration: underline;
    }
    
    .feedback-section .markdown-content :global(blockquote) {
        padding: 12px 16px;
        margin: 12px 0;
        border-left: 4px solid #3B82F6;
        background-color: #f5f5f5;
        color: #555;
    }
    
    .feedback-section .markdown-content :global(hr) {
        height: 1px;
        background-color: #e0e0e0;
        border: none;
        margin: 16px 0;
    }
    
    .feedback-section .markdown-content :global(table) {
        border-collapse: collapse;
        width: 100%;
        margin: 12px 0;
    }
    
    .feedback-section .markdown-content :global(th),
    .feedback-section .markdown-content :global(td) {
        border: 1px solid #eee;
        padding: 8px;
        text-align: left;
    }
    
    .feedback-section .markdown-content :global(th) {
        background-color: #f0f0f0;
        font-weight: 600;
    }

    /* Styles for diff view */
    .diff-view {
        white-space: pre-wrap;
        word-wrap: break-word;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        background-color: #f0f0f0;
        padding: 12px;
        border-radius: 6px;
        overflow-x: auto;
    }
    
    /* Status message styles */
    .status-message {
        padding: 12px;
        margin-bottom: 12px;
        border-radius: 6px;
        background-color: #f0f0f0;
    }
    
    .status-message.error {
        background-color: #ffe6e6;
        color: #8b0000;
    }
    .diff-part.added {
        background-color: #cbe1d1;
        color: #006400;
    }
    .diff-part.removed {
        background-color: #ffebe9;
        color: #b30000;
        text-decoration: line-through;
    }
    .diff-part.common {
        color: #333;
        background-color: #fcfcfc;
        padding: 0 2px;
    }
</style>
