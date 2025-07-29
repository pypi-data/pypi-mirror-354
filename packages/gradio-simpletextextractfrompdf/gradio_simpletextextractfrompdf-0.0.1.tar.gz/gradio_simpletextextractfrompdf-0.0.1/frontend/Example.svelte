<script lang="ts">
	import PDFuploadAndExtract from "./shared/components/PDFuploadAndExtract.svelte";
	import PDFviewer from "./shared/components/PDFviewer.svelte";
	import TextContentViewer from "./shared/components/TextContentViewer.svelte";
	

	export let value: string;
    export let type: "gallery" | "table";
    export let selected = false;
</script>

<div
	class:table={type === "table"}
	class:gallery={type === "gallery"}
	class:selected
>
	{value}
	<PDFuploadAndExtract/>
	<PDFviewer/>
	<TextContentViewer textContent={value}/>

</div>

<style>
	.gallery {
		padding: var(--size-1) var(--size-2);
	}
</style>
