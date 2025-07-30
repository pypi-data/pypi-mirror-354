<script>
    export let textContent
    let showTextContent = true
</script>



<button class="button" on:click={() => showTextContent = !showTextContent}>
    {showTextContent ? "Hide Text" : "Show Text"}
</button>
{#if showTextContent}
    <div class="scrollable-content">
        {#if textContent}
         {textContent}
        {:else}
            <p style="text-align: center;">The Extracted Text Will Appear Here</p>
        {/if}
    </div>
{/if}

<style>
.scrollable-content {
    max-height: 350px;
    overflow-y: auto;
    border: 1px solid #e5e7eb; /* light gray */
    border-radius: 0.5rem;
    padding: 1rem;
    background: #fafbfc;
    font-family: inherit;
    font-size: 1rem;
    color: #222;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    transition: box-shadow 0.2s;
    margin-top: 1rem;
}
.scrollable-content:focus-within, .scrollable-content:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-color: #b6bbc4;
}

.button {
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid #bbb;
    background: #f5f5f5;
    cursor: pointer;
    margin-top: 0.5rem;
}
</style>