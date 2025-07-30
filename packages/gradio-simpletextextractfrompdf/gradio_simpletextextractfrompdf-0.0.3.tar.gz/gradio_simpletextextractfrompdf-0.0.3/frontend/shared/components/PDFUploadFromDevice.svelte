<script lang="ts">
import * as pdfjsLib from 'pdfjs-dist';
import 'pdfjs-dist/build/pdf.worker.min.mjs';

import { createEventDispatcher } from "svelte";

pdfjsLib.GlobalWorkerOptions.workerSrc =  "https://cdn.bootcss.com/pdf.js/3.11.174/pdf.worker.js";

const dispatch = createEventDispatcher();

let selectedFiles: File[] = [];
let selectedFilesText: string[] = [];
let fileNames: string[] = [];
let progressStatus: string = "";
let errorMessage: string = "";

function handleFileSelect(event: Event) {
    errorMessage = "";
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
        selectedFiles = Array.from(input.files);
        fileNames = selectedFiles.map(f => f.name);
        errorMessage = "";
        progressStatus = "";
    }
    // Reset input so the same files can be selected again
    input.value = "";
}

async function dispatchUpload() {
    progressStatus = "Checking files...";
    errorMessage = "";
    selectedFilesText = [];

    if (selectedFiles.length === 0) {
        progressStatus = "";
        errorMessage = "No files selected. Please select files to upload.";
        return;
    }

    for (const file of selectedFiles) {
        if (file.type !== "application/pdf") {
            errorMessage = `The file ${file.name} is not a PDF file.`;
            continue;
        }
        const text = await extractTextFromPDF(file);
        if (!text) {
            errorMessage = `No text found in ${file.name}.`;
            continue;
        }
        selectedFilesText.push(text);
    }

    if (selectedFilesText.length > 0) {
        // Combine all the extracted text into a single string, with file names
        dispatch("upload", {
            content: {
                asString: selectedFilesText.map((text, i) => `## ${fileNames[i]}\n${text}`).join('\n\n'),
                asFiles: selectedFiles
            },
            type: "pdf",
        });
        progressStatus = "Text extracted successfully";
    } else {
        progressStatus = "";
    }
}

async function extractTextFromPDF(file: File): Promise<string> {
    if (!pdfjsLib) {
        console.log("pdfjsLib is not initialized");
        return "";
    }
    if (!file) {
        console.log("no file input");
        return "";
    }
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    let text = '';
    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
        const page = await pdf.getPage(pageNum);
        const textContent = await page.getTextContent();
        const pageText = textContent.items.map(item => (item as any).str).join(' ');
        text += pageText + '\n\n';
    }
    return text.trim();
}
</script>

<div class="upload-container">
    <input 
        type="file" 
        accept=".pdf"
        class="file-input" 
        id="file-upload"
        multiple
        on:change={handleFileSelect}
    />
    <label for="file-upload" class="file-label">
        <div class="label-content">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <div class="upload-text">
                <span class="upload-text-main">Click to upload</span>
            </div>
            {#if errorMessage}
                <p class="error-message">{errorMessage}</p>
            {:else}
                <p class="file-type-info">PDF files only</p>
            {/if}
            {#if fileNames.length}
                <ul>
                    {#each fileNames as name}
                        <li class="file-name">{name}</li>
                    {/each}
                </ul>
            {/if}
            {#if progressStatus}
                <p class="progess-status">{progressStatus}</p>
            {/if}
        </div>
    </label>
</div>
{#if selectedFiles.length}
<div class="action-buttons">
    <button 
        class="cancel-button"
        on:click={() => {
            selectedFiles = [];
            selectedFilesText = [];
            fileNames = [];
            errorMessage = "";
            progressStatus = "";
        }}
    >
        Cancel
    </button>
    <button 
        class="upload-button"
        on:click={dispatchUpload}
    >
        Upload and Extract Text
    </button>
</div>
{/if}

<style>
.upload-container {
    border-width: 2px;
    border-style: dashed;
    border-color: #d1d5db; /* gray-300 */
    border-radius: 0.5rem;
    padding: 2rem;
    text-align: center;
}
.file-input {
    display: none;
}
.file-label {
    cursor: pointer;
}
.label-content > :global(* + *) {
    margin-top: 1rem;
}
.icon {
    height: 3rem;
    width: 3rem;
    margin-left: auto;
    margin-right: auto;
    color: #9ca3af; /* gray-400 */
}
.upload-text {
    color: #4b5563; /* gray-600 */
}
.upload-text-main {
    font-weight: 500;
}
.error-message {
    font-size: 0.875rem;
    line-height: 1.25rem;
    color: #ef4444; /* red-500 */
}
.file-type-info {
    font-size: 0.875rem;
    line-height: 1.25rem;
    color: #6b7281; /* gray-500 */
}
.file-name {
    font-size: 0.875rem;
    line-height: 1.25rem;
    color: #3b82f6; /* blue-500 */
}
.action-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 0.5rem;
    gap: 1rem;
}
.cancel-button {
    padding: 0.5rem 1rem;
    color: #374151; /* gray-700 */
    background-color: #e5e7eb; /* gray-200 */
    border-radius: 0.5rem;
    border: none;
}
.cancel-button:hover {
    background-color: #d1d5db; /* gray-300 */
}
.cancel-button:focus {
    outline: 2px solid transparent;
    outline-offset: 2px;
    box-shadow: 0 0 0 2px #6b7281; /* ring-gray-500 */
}
.upload-button {
    padding: 0.5rem 1rem;
    color: #ffffff; /* white */
    background-color: #3b82f6; /* blue-500 */
    border-radius: 0.5rem;
    border: none;
}
.upload-button:hover {
    background-color: #2563eb; /* blue-600 */
    cursor: pointer;
}
.upload-button:focus {
    outline: 2px solid transparent;
    outline-offset: 2px;
    box-shadow: 0 0 0 2px #3b82f6; /* ring-blue-500 */
}
.upload-button:disabled {
    background-color: #93c5fd; /* blue-300 */
    cursor: not-allowed;
}
.progess-status {
    font-size: 0.875rem;
    line-height: 1.25rem;
    color: #10b981; /* emerald-500 */
}
</style>