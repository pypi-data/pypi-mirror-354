<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import type { FileData } from "@gradio/client";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import OverlayPlayer from "./shared/OverlayPlayer.svelte";

	export let value: { video: { file: FileData } | null; json_data: string | null } | null = null;
	export let gradio: Gradio;
    // Unused props can be kept for Gradio compatibility, the warnings are harmless
    export let elem_id = "", elem_classes = [], visible = true, loading_status: LoadingStatus, height, width, container, scale, min_width;
	export let autoplay = false, loop = false;

	let video_url: string | null | undefined;
	let json_content: string | null | undefined;

	$: {
		if (value) {
			video_url = value.video?.url;
			json_content = value.json_data;
		} else {
			video_url = null;
			json_content = null;
		}
	}
</script>

<Block {visible} {elem_id} {elem_classes} {height} {width} {container} {scale} {min_width} allow_overflow={false}>
	<StatusTracker {...loading_status} autoscroll={gradio.autoscroll} i18n={gradio.i18n} />
	{#if json_content}
		<OverlayPlayer
			video_src={video_url}
			json_data_str={json_content}
			{autoplay}
			{loop}
		/>
	{/if}
</Block>