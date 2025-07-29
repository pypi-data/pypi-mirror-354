<script lang="ts">
	import { createEventDispatcher } from "svelte";
	import { Upload } from "@gradio/upload";
	import type { FileData, Client } from "@gradio/client";
	import { BlockLabel } from "@gradio/atoms";
	import { Video } from "@gradio/icons";
	import OverlayPlayer from "./OverlayPlayer.svelte";
	import type { I18nFormatter } from "@gradio/utils";

	// Props for video
	export let value: FileData | null = null;
	// REMOVED `sources` prop as it was unused.
	export let label: string | undefined = "Interactive Video with Overlay";
	export let show_label = true;
	export let autoplay = false;
	export let root: string;
	export let i18n: I18nFormatter;
	export let upload: Client["upload"];
	export let loop: boolean;
	export let uploading = false;

	// Props for JSON overlay data
	export let json: FileData | null = null;

	const dispatch = createEventDispatcher<{
		change: { video: FileData | null; json: FileData | null };
		clear?: never;
		play?: never;
		pause?: never;
		end?: never;
		drag: boolean;
		error: string;
		upload: { video?: FileData; json?: FileData };
	}>();

	function handle_video_load({ detail }: CustomEvent<FileData | null>): void {
		value = detail;
		dispatch("change", { video: value, json });
		if (detail) dispatch("upload", { video: detail });
	}

	function handle_json_load({ detail }: CustomEvent<FileData | null>): void {
		json = detail;
		dispatch("change", { video: value, json });
		if (detail) dispatch("upload", { json: detail });
	}

	function handle_clear(): void {
		value = null;
		json = null;
		dispatch("change", { video: null, json: null });
		dispatch("clear");
	}

	let dragging = false;
	$: dispatch("drag", dragging);
</script>

<BlockLabel {show_label} Icon={Video} {label} />

<div class="component-container">
	{#if value === null}
		<div class="upload-container">
			<Upload
				bind:dragging
				bind:uploading
				filetype="video/x-m4v,video/*"
				on:load={handle_video_load}
				on:error={({ detail }) => dispatch("error", detail)}
				{root}
				{upload}
				aria_label={i18n("video.drop_to_upload")}
			>
				Drop Video Here
			</Upload>
		</div>
	{:else if !json}
        <div class="upload-container">
			<Upload
				bind:dragging
				filetype="application/json"
				on:load={handle_json_load}
				on:error={({ detail }) => dispatch("error", detail)}
				{root}
				{upload}
				aria_label="Drop JSON here"
			>
				Drop JSON Overlay Data Here
			</Upload>
		</div>
    {/if}

	{#if value && json}
		<OverlayPlayer
			video_src={value.url}
			json_src={json.url}
			{autoplay}
			{loop}
			on:play
			on:pause
			on:end
			on:error
		/>
	{/if}
</div>

<style>
	.component-container {
		display: flex;
		flex-direction: column;
		gap: var(--size-4);
		height: 100%;
		width: 100%;
	}
	.upload-container {
		display: flex;
        flex-direction: column;
		min-height: var(--size-60);
        align-items: center;
        justify-content: center;
		border: 1px dashed var(--border-color-primary);
		border-radius: var(--radius-lg);
	}
</style>