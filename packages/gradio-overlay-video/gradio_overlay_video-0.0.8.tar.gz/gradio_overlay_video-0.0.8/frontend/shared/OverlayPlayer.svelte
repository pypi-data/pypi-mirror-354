<script lang="ts">
    import { createEventDispatcher, onMount } from "svelte";
    import { Play, Pause } from "@gradio/icons";
    import Video from "./Video.svelte";
    import { format_time } from "@gradio/utils";

    export let video_src: string | undefined | null = undefined;
    export let json_data_str: string | undefined | null = undefined;
    export let autoplay: boolean;
    export let loop: boolean;

    let time = 0,
        duration: number,
        paused = true,
        video: HTMLVideoElement,
        canvas: HTMLCanvasElement;
    let frame_data: any[] = [],
        video_info: any = {},
        capabilities: any = {};
    let frame_slider_value = 0,
        current_frame_index = 0,
        fps = 30;
    let show_video = false,
        show_joints: boolean,
        show_bones: boolean,
        show_laban: boolean,
        show_direction_arrows: boolean,
        show_motion_trails: boolean;
    let json_playing = false,
        json_play_interval: any = null;
    let player_container: HTMLDivElement;

    // Parse the streamlined visualization data from backend
    $: if (json_data_str) {
        try {
            const data = JSON.parse(json_data_str);
            video_info = data.video_info || {};
            frame_data = data.frames || [];
            fps = data.fps || 30;
            capabilities = data.capabilities || {};


            // Set defaults only once when capabilities are first loaded
            if (show_joints === undefined) {
                show_joints = capabilities.has_joints !== false;
                show_bones = capabilities.has_bones !== false;
                show_direction_arrows =
                    capabilities.has_direction_arrows !== false;
                show_motion_trails = capabilities.has_motion_trails !== false;
                // Disable Laban by default as requested
                show_laban = false;
            }

            if (!video_src) {
                duration = video_info.duration_seconds || 0;
            }
        } catch (e) {
            console.error("Failed to parse JSON data:", e);
        }
    }

    // Set aspect ratio CSS variable for proper player container sizing
    $: if (player_container && video_info.width && video_info.height) {
        const aspectRatio = video_info.width / video_info.height;
        player_container.style.setProperty(
            "--player-aspect-ratio",
            `${aspectRatio}`,
        );
    }

    // Update current frame index based on video time or slider
    $: {
        if (show_video && frame_data.length > 0 && time !== undefined) {
            current_frame_index = frame_data.findIndex(
                (d) =>
                    time >= d.timestamp &&
                    (frame_data[frame_data.indexOf(d) + 1]
                        ? time < frame_data[frame_data.indexOf(d) + 1].timestamp
                        : true),
            );
        } else if (!show_video) {
            current_frame_index = frame_slider_value;
        }
    }
    
    // Redraw when frame index or time changes
    $: if (canvas && (current_frame_index >= 0 || time >= 0)) {
        draw();
    }

    function draw() {
        if (!canvas || frame_data.length === 0) return;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        // Prioritize video_info dimensions for aspect ratio to avoid skewing
        let ar =
            video_info.height && video_info.width
                ? video_info.height / video_info.width
                : video && video.videoHeight > 0
                  ? video.videoHeight / video.videoWidth
                  : 9 / 16;

        if (canvas.parentElement) {
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.width * ar;
        }

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const current_frame = frame_data[current_frame_index];
        if (!current_frame) return;

        const scaleX = canvas.width,
            scaleY = canvas.height;

        // Draw motion trails if enabled and available
        if (show_motion_trails && current_frame.motion_trail) {
            current_frame.motion_trail.forEach((segment: any) => {
                const alpha = segment.alpha || 0.5;
                ctx.strokeStyle = `rgba(138, 43, 226, ${alpha})`;
                ctx.lineWidth = Math.max(1, 3 * alpha);

                ctx.beginPath();
                ctx.moveTo(segment.start.x * scaleX, segment.start.y * scaleY);
                ctx.lineTo(segment.end.x * scaleX, segment.end.y * scaleY);
                ctx.stroke();
            });
        }

        // Draw bones if enabled and available
        if (show_bones && current_frame.bones) {
            current_frame.bones.forEach((bone: any) => {
                // Viridian bones with gradient effect
                const startX = bone.start.x * scaleX;
                const startY = bone.start.y * scaleY;
                const endX = bone.end.x * scaleX;
                const endY = bone.end.y * scaleY;
                
                // Create gradient for bone
                const gradient = ctx.createLinearGradient(startX, startY, endX, endY);
                gradient.addColorStop(0, "rgba(64, 130, 109, 0.9)");  // Viridian
                gradient.addColorStop(0.5, "rgba(60, 140, 100, 1.0)");
                gradient.addColorStop(1, "rgba(65, 132, 110, 0.88)");
                
                // Glow effect
                ctx.shadowColor = "rgba(64, 130, 109, 0.5)";
                ctx.shadowBlur = 6;
                
                ctx.strokeStyle = gradient;
                ctx.lineWidth = 2;
                ctx.lineCap = "round";
                
                ctx.beginPath();
                ctx.moveTo(startX, startY);
                ctx.lineTo(endX, endY);
                ctx.stroke();
                
                // Reset shadow
                ctx.shadowBlur = 0;
            });
        }

        // Draw joints if enabled and available
        if (show_joints && current_frame.joints) {
            current_frame.joints.forEach((joint: any) => {
                // Violet joints with confidence-based alpha
                const confidence = joint.confidence || 1;
                const alpha = Math.max(0.4, confidence);
                const radius = Math.max(1, 3 * confidence);
                
                // Outer glow effect
                ctx.shadowColor = "rgba(64, 130, 109, 0.5)";
                ctx.shadowBlur = 8;
                
                ctx.fillStyle = `rgba(138, 43, 226, ${alpha})`; // Violet
                ctx.beginPath();
                ctx.arc(joint.x * scaleX, joint.y * scaleY, radius, 0, 2 * Math.PI);
                ctx.fill();

                // Reset shadow
                ctx.shadowBlur = 0;
                
                // Bright border for contrast
                ctx.strokeStyle = "rgba(64, 130, 109, 0.9)";
                ctx.lineWidth = 1.5;
                ctx.stroke();
            });
        }

        // Draw direction arrows if enabled and available
        if (show_direction_arrows && current_frame.direction_arrow) {
            const arrow = current_frame.direction_arrow;
            const intensity_colors = {
                low: { color: "rgba(0, 255, 127, 0.9)", glow: "rgba(0, 255, 127, 0.4)" },    // Spring green
                medium: { color: "rgba(255, 140, 0, 0.9)", glow: "rgba(255, 140, 0, 0.4)" }, // Dark orange
                high: { color: "rgba(255, 20, 147, 0.9)", glow: "rgba(255, 20, 147, 0.4)" }   // Deep pink
            };

            const arrowStyle = intensity_colors[arrow.intensity as keyof typeof intensity_colors] || 
                { color: "rgba(255, 255, 255, 0.9)", glow: "rgba(255, 255, 255, 0.4)" };

            const startX = arrow.start.x * scaleX;
            const startY = arrow.start.y * scaleY;
            const endX = arrow.end.x * scaleX;
            const endY = arrow.end.y * scaleY;
            const angle = Math.atan2(endY - startY, endX - startX);
            
            // arrow with glow and gradient
            ctx.shadowColor = arrowStyle.glow;
            ctx.shadowBlur = 12;
            
            // Create gradient along arrow direction
            const gradient = ctx.createLinearGradient(startX, startY, endX, endY);
            gradient.addColorStop(0, arrowStyle.color.replace('0.9', '0.6'));
            gradient.addColorStop(0.7, arrowStyle.color);
            gradient.addColorStop(1, arrowStyle.color.replace('0.9', '1.0'));
            
            ctx.strokeStyle = gradient;
            ctx.lineWidth = 4;
            ctx.lineCap = "round";

            // Draw arrow shaft with elegant styling
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(endX, endY);
            ctx.stroke();

            // Draw enhanced arrow head
            const headlen = 18;
            const headWidth = Math.PI / 5; // Slightly wider head
            
            ctx.fillStyle = arrowStyle.color;
            ctx.beginPath();
            ctx.moveTo(endX, endY);
            ctx.lineTo(
                endX - headlen * Math.cos(angle - headWidth),
                endY - headlen * Math.sin(angle - headWidth)
            );
            ctx.lineTo(
                endX - headlen * 0.6 * Math.cos(angle),
                endY - headlen * 0.6 * Math.sin(angle)
            );
            ctx.lineTo(
                endX - headlen * Math.cos(angle + headWidth),
                endY - headlen * Math.sin(angle + headWidth)
            );
            ctx.closePath();
            ctx.fill();
            
            // Reset shadow
            ctx.shadowBlur = 0;
        }
    }

    // JSON-only playback logic using FPS from data
    function play_json() {
        if (json_playing || frame_data.length <= 1) return;
        json_playing = true;
        json_play_interval = setInterval(() => {
            if (frame_slider_value < frame_data.length - 1) {
                frame_slider_value += 1;
            } else {
                frame_slider_value = 0;
            }
        }, 1000 / fps); // Use FPS from processed data
    }
    function pause_json() {
        json_playing = false;
        if (json_play_interval) clearInterval(json_play_interval);
    }

    $: if (!show_video && json_playing) play_json();
    $: if (!json_playing) pause_json();

    // Handle video time updates
    function handleTimeUpdate() {
        if (video) {
            time = video.currentTime;
        }
    }

    onMount(() => {
        return () => {
            // Cleanup event listeners when component unmounts
            if (video) {
                video.removeEventListener("timeupdate", handleTimeUpdate);
            }
        };
    });

    // Add event listener when video element is available
    $: if (video) {
        video.addEventListener("timeupdate", handleTimeUpdate);
    }
</script>

<div class="wrap">
    <div class="player-container" bind:this={player_container}>
        {#if video_src && show_video}
            <Video
                src={video_src}
                is_stream={false}
                preload="auto"
                {autoplay}
                {loop}
                on:click={() => (paused ? video.play() : video.pause())}
                on:play
                on:pause
                bind:currentTime={time}
                bind:duration
                bind:paused
                bind:node={video}
            />
        {/if}
        <canvas bind:this={canvas} class="overlay-canvas"></canvas>
        {#if show_laban && frame_data[current_frame_index]?.laban_metrics}
            <div class="laban-overlay">
                {#each Object.entries(frame_data[current_frame_index].laban_metrics) as [key, value]}
                    <div>
                        <span class="metric-label">{key.replace(/_/g, ' ')}:</span>
                        <span class="metric-value">
                            {#if typeof value === 'object'}
                                {JSON.stringify(value)}
                            {:else if typeof value === 'number'}
                                {value.toFixed(2)}
                            {:else}
                                {value}
                            {/if}
                        </span>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
    <div class="controls">
        <div class="inner">
            {#if show_video}
                <button
                    class="icon"
                    on:click={() => (paused ? video.play() : video.pause())}
                    aria-label="Play/Pause"
                    >{#if paused}<Play />{:else}<Pause />{/if}</button
                >
                <span class="time"
                    >{format_time(time)} / {format_time(duration || 0)}</span
                >
                <progress value={time / duration || 0} />
            {:else}
                <button
                    class="icon"
                    on:click={() => (json_playing ? pause_json() : play_json())}
                    aria-label="Play/Pause"
                    >{#if !json_playing}<Play />{:else}<Pause />{/if}</button
                >
                <span class="time"
                    >{(frame_data[frame_slider_value]?.timestamp || 0).toFixed(
                        2,
                    )}s</span
                >
                <input
                    type="range"
                    min="0"
                    max={frame_data.length > 1 ? frame_data.length - 1 : 1}
                    bind:value={frame_slider_value}
                    class="frame-slider"
                />
                <span class="time">{(duration || 0).toFixed(2)}s</span>
            {/if}
        </div>
        <div class="checkbox-row">
            <div class="checkbox-container">
                {#if video_src}
                    <input type="checkbox" id="show-video" bind:checked={show_video} />
                    <label for="show-video">Video</label>
                {/if}
                <input type="checkbox" id="show-joints" bind:checked={show_joints} />
                <label for="show-joints">Joints</label>
                <input type="checkbox" id="show-bones" bind:checked={show_bones} />
                <label for="show-bones">Bones</label>
                <input type="checkbox" id="show-direction-arrows" bind:checked={show_direction_arrows} />
                <label for="show-direction-arrows">Arrows</label>
                <input type="checkbox" id="show-motion-trails" bind:checked={show_motion_trails} />
                <label for="show-motion-trails">Trails</label>
                <input type="checkbox" id="show-laban" bind:checked={show_laban} />
                <label for="show-laban">Laban</label>
            </div>
        </div>
    </div>
</div>

<style>
    .wrap {
        position: relative;
        background: linear-gradient(135deg, var(--background-fill-secondary) 0%, var(--background-fill-primary) 100%);
        height: 100%;
        width: 100%;
        border-radius: var(--radius-xl);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .player-container {
        position: relative;
        width: 100%;
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 420px;
        max-height: 780px;
        flex: 1 1 auto;
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
        overflow: hidden;
    }
    .player-container:not(:has(video)) {
        aspect-ratio: var(--player-aspect-ratio, 16 / 9);
    }
    :global(.player-container video) {
        display: block;
        height: 100%;
        width: 100%;
    }
    .overlay-canvas {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
    }
    .controls {
        width: 100%;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        flex-direction: column;
        align-items: stretch;
        padding-bottom: 0;
        flex: 0 0 auto;
        box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.15);
    }
    .inner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px var(--size-4);
        width: 100%;
        min-height: 48px;
        color: white;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .icon {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        padding: 8px;
        margin: 0;
        color: white;
        cursor: pointer;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
        backdrop-filter: blur(5px);
    }
    .icon:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
        transform: scale(1.05);
    }
    .icon:active {
        transform: scale(0.95);
    }
    .time {
        margin: 0 var(--size-3);
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
        font-size: var(--text-sm);
        font-weight: 500;
        color: rgba(255, 255, 255, 0.9);
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }
    progress,
    .frame-slider {
        flex-grow: 1;
        margin: 0 var(--size-4);
    }
    .checkbox-row {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.05) 100%);
        padding: 12px 0 14px 0;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    .checkbox-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 24px;
        background: none;
    }
    .checkbox-container label {
        user-select: none;
        font-size: var(--text-sm);
        font-weight: 500;
        cursor: pointer;
        margin-right: 8px;
        margin-left: 2px;
        color: rgba(255, 255, 255, 0.85);
        transition: color 0.2s ease;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }
    .checkbox-container label:hover {
        color: rgba(255, 255, 255, 1);
    }
    .checkbox-container input[type="checkbox"] {
        width: 18px;
        height: 18px;
        appearance: none;
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 4px;
        cursor: pointer;
        position: relative;
        transition: all 0.2s ease;
        backdrop-filter: blur(5px);
    }
    .checkbox-container input[type="checkbox"]:checked {
        background: linear-gradient(135deg, var(--color-accent, #8b5cf6) 0%, var(--color-accent-soft, #a78bfa) 100%);
        border-color: var(--color-accent, #8b5cf6);
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
    }
    .checkbox-container input[type="checkbox"]:checked::after {
        content: '✓';
        position: absolute;
        top: -1px;
        left: 2px;
        color: white;
        font-size: 12px;
        font-weight: bold;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }
    .checkbox-container input[type="checkbox"]:hover {
        border-color: rgba(255, 255, 255, 0.5);
        transform: scale(1.05);
    }
    .checkbox-container input[type="checkbox"]:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    .laban-overlay {
        position: absolute;
        top: 16px;
        left: 16px;
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9) 0%, rgba(20, 20, 20, 0.9) 100%);
        color: #fff;
        padding: 14px 18px;
        border-radius: 12px;
        font-size: 13px;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        z-index: 10;
        pointer-events: none;
        min-width: 200px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .laban-overlay > div {
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 2px 0;
    }
    .laban-overlay > div:last-child {
        margin-bottom: 0;
    }
    .laban-overlay > div:not(:last-child) {
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 6px;
    }
    .metric-label {
        font-weight: 600;
        text-transform: capitalize;
        color: rgba(255, 255, 255, 0.7);
        margin-right: 12px;
        min-width: 90px;
        font-size: 12px;
        letter-spacing: 0.025em;
    }
    .metric-value {
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
        color: rgba(255, 255, 255, 0.95);
        text-align: right;
        font-weight: 500;
        font-size: 12px;
        background: rgba(255, 255, 255, 0.05);
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* Enhanced slider styling */
    .timeline-slider::-webkit-slider-thumb,
    .frame-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--color-accent, #8b5cf6) 0%, var(--color-accent-soft, #a78bfa) 100%);
        cursor: pointer;
        border: 2px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
        transition: all 0.2s ease;
    }
    
    .timeline-slider::-webkit-slider-thumb:hover,
    .frame-slider::-webkit-slider-thumb:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    }
</style>
