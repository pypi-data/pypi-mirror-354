<script lang="ts">
    export let files: File[] | null = null

    let showPDF = true
    let currentFile: File | null = null

    $: if (files) {
        currentFile = files[0]
    }
</script>

<button class="button" on:click={() => showPDF = !showPDF}>
    {showPDF ? "Hide PDF" : "Show PDF"}
</button>

{#if currentFile && showPDF}
    <div class="pdf-viewer-container">
        <object
            data={URL.createObjectURL(currentFile)}
            type="application/pdf"
            class="pdf-object"
            title="Resume PDF Viewer"
            aria-label="PDF resume document viewer"
            role="document"
        >
            <p>Your browser doesn't support PDF viewing. <a href={URL.createObjectURL(currentFile)} target="_blank" aria-label="Download resume PDF" title="Download PDF">Click here to download the PDF</a>.</p>
        </object>
    </div>
{/if}
{#if !currentFile}
    <div class="container">
        <p>The PDF will appear here</p>
    </div>
{/if}


<style>
.pdf-viewer-container {
    width: 100%;
    height: 70vh;
    min-height: 400px;
    max-height: 80vh;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    background: #fafbfc;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    overflow: hidden;
    margin-top: 1rem;
}
.pdf-object {
    width: 100%;
    height: 100%;
    border: none;
    background: transparent;
    min-height: 400px;
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
.container {
    width: 100%;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    margin-top: 0.5rem;
}
</style>