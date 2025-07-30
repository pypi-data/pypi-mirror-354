<script lang="ts">
	import UploadAndExtract from "./shared/components/UploadAndExtract.svelte";
	import PDFviewer from "./shared/components/PDFviewer.svelte";
	import TextContentViewer from "./shared/components/TextContentViewer.svelte";

	import type { Gradio } from "@gradio/utils";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: string;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let gradio: Gradio<{
		change: never;
		clear_status: LoadingStatus;
	}>;

	let files: File[] = []

	
	function handleUpload(event: CustomEvent<{content: {asString: string, asFiles: File[]}, type: string}>) {
		let {content: {asString, asFiles }} = event.detail

		value = asString
		files = asFiles
	}

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

		<UploadAndExtract on:upload={handleUpload} />
		<TextContentViewer bind:textContent={value}/>
		<PDFviewer {files}/>

	<p class="value-status">{value ? "Value is set ✅" : "Value is not set ❌"}</p>
	
</Block>

<style>
	.value-status {
		display: inline-block;
		font-size: 0.85rem;
		color: #fff;
		background: #888;
		padding: 0.1em 0.5em;
		border-radius: 999px;
		margin-top: 1em;
		vertical-align: middle;
		letter-spacing: 0.02em;
		font-weight: 500;
	}
</style>
