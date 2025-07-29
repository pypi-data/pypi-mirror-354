<svelte:options accessors={true}/>

<script lang="ts">
    import type {Gradio} from "@gradio/utils";
    import {Block, BlockTitle} from "@gradio/atoms";
    import type {LoadingStatus} from "@gradio/statustracker";
    import {StatusTracker} from "@gradio/statustracker";
    import {onMount, tick} from "svelte";
    import {Client, type FileData, prepare_files} from "@gradio/client";

    export let gradio: Gradio<{
        change: never;
        submit: never;
        input: never;
        upload: never;
        clear_status: LoadingStatus;
    }>;
    export let label = "Audio-Grid";
    export let elem_id = "";
    export let elem_classes: string[] = [];
    export let visible = true;
    export let value: Array<FileData> = [];
    export let show_label: boolean;
    export let scale: number | null = null;
    export let min_width: number | undefined = undefined;
    export let loading_status: LoadingStatus | undefined = undefined;
    export let value_is_output = false;
    export let interactive: boolean;
    export let root: string;

    // Add the missing props that are being passed to prevent unknown prop warnings
    export const target: any = undefined;
    export const key: any = undefined;
    export const name: any = undefined;
    export const attached_events: any = undefined;
    export const server: any = undefined;

    let draggedIndex: number | null = null;
    let fileInputs: HTMLInputElement[] = [];

    let client: Client;

    onMount(async () => {
        client = await Client.connect(root);
    });

    function handle_change(): void {
        gradio.dispatch("change");
        if (!value_is_output) {
            gradio.dispatch("input");
        }
    }

    function handle_upload(): void {
        gradio.dispatch("upload");
    }

    function removeFile(index: number): void {
        if (interactive) {
            value = value.filter((_, i) => i !== index);
            handle_change();
        }
    }

    async function handleFileChange(event: Event): Promise<void> {
        if (!interactive) return;
        const input = event.target as HTMLInputElement;
        let newFiles = await loadFiles(input.files)
        value = [...value, ...newFiles];
        await tick();
        handle_change();
        await tick();
        handle_upload();
    }

    function handleDragStart(event: DragEvent, index: number): void {
        if (!interactive) return;
        draggedIndex = index;
        if (event.dataTransfer) {
            event.dataTransfer.effectAllowed = "move";
            event.dataTransfer.setData("text/html", "");
        }
    }

    function handleDragOver(event: DragEvent): void {
        if (!interactive) return;
        event.preventDefault();
        if (event.dataTransfer) {
            event.dataTransfer.dropEffect = "move";
        }
    }

    function handleGridDrop(event: DragEvent): void {
        if (!interactive || draggedIndex === null) return;
        event.preventDefault();

        // Get the grid element and its bounding rect
        const gridElement = event.currentTarget as HTMLElement;
        const gridRect = gridElement.getBoundingClientRect();

        // Calculate drop position relative to grid
        const dropX = event.clientX - gridRect.left;
        const dropY = event.clientY - gridRect.top;

        // Get all squares and calculate which position to insert at
        const squares = gridElement.querySelectorAll('.upload-square');
        let insertIndex = value.length;

        for (let i = 0; i < squares.length; i++) {
            const square = squares[i] as HTMLElement;
            const squareRect = square.getBoundingClientRect();
            const squareX = squareRect.left - gridRect.left;
            const squareY = squareRect.top - gridRect.top;

            // If drop position is before this square (left or above), insert here
            if (dropY < squareY || (dropY < squareY + squareRect.height && dropX < squareX + squareRect.width / 2)) {
                insertIndex = i;
                break;
            }
        }

        // Don't move if dropping in the same position
        if (insertIndex === draggedIndex || insertIndex === draggedIndex + 1) {
            draggedIndex = null;
            return;
        }

        // Perform the reordering
        const draggedItem = value[draggedIndex];
        const newValue = [...value];

        // Remove the dragged item
        newValue.splice(draggedIndex, 1);

        // Adjust insert index if we removed an item before it
        const actualInsertIndex = draggedIndex < insertIndex ? insertIndex - 1 : insertIndex;

        // Insert at the new position
        newValue.splice(actualInsertIndex, 0, draggedItem);

        value = newValue;
        draggedIndex = null;
        handle_change();
    }

    function handleSquareDrop(event: DragEvent, dropIndex: number): void {
        if (!interactive || draggedIndex === null) return;
        event.preventDefault();
        event.stopPropagation(); // Prevent grid drop from also firing

        // Don't do anything if dropping on the same square
        if (draggedIndex === dropIndex) {
            draggedIndex = null;
            return;
        }

        const draggedItem = value[draggedIndex];
        const newValue = [...value];

        // Check if we're dropping on an existing file (swap) or empty slot (insert)
        if (value[dropIndex]) {
            // Swap positions when dropping on another file
            newValue[draggedIndex] = value[dropIndex];
            newValue[dropIndex] = draggedItem;
        } else {
            // Insert behavior when dropping on empty slot
            // Remove the dragged item
            newValue.splice(draggedIndex, 1);

            // Insert at new position (adjust index if dragged from before drop position)
            const actualDropIndex = draggedIndex < dropIndex ? dropIndex - 1 : dropIndex;
            newValue.splice(actualDropIndex, 0, draggedItem);
        }

        value = newValue;
        draggedIndex = null;
        handle_change();
    }

    function handleDragEnd(): void {
        draggedIndex = null;
    }

    async function upload_to_server(file_data: FileData[]): Promise<FileData[]> {
        await tick();
        return await client.upload(file_data, root)
    }

    async function loadFiles(files: FileList): Promise<FileData[]> {
        let _files: File[] = Array.from(files);

        if (!files.length) {
            return;
        }

        let file_data = await prepare_files(_files);
        return await upload_to_server(file_data);
    }

    async function handleFileDrop(event: DragEvent): Promise<void> {
        if (!interactive) return;
        event.preventDefault();
        const files = event.dataTransfer?.files;
        let loaded_files = await loadFiles(files)
        value = [...value, ...loaded_files];
        await tick();
        handle_change();
        await tick();
        handle_upload();
    }

    function getFileName(file: FileData): string {
        return file?.orig_name || 'Unknown File';
    }
</script>

<Block
        {visible}
        {elem_id}
        {elem_classes}
        {scale}
        {min_width}
        allow_overflow={false}
        padding={true}
>
    <slot/>

    {#if loading_status}
        <StatusTracker
                autoscroll={gradio.autoscroll}
                i18n={gradio.i18n}
                {...loading_status}
                on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
        />
    {/if}

    <div class="audio-upload-container">
        <BlockTitle {root} {show_label} info={undefined}>{label}</BlockTitle>

        <div
                class="upload-grid"
                role="application"
                aria-label="Audio file upload area"
                on:dragover={handleDragOver}
                on:drop={handleGridDrop}
        >
            {#each value as fileObj, index (index)}
                <div
                        class="upload-square"
                        class:dragging={draggedIndex === index}
                        class:has-file={fileObj}
                        draggable={interactive && !!fileObj}
                        on:dragstart={(e) => handleDragStart(e, index)}
                        on:dragover={handleDragOver}
                        on:drop={(e) => handleSquareDrop(e, index)}
                        on:dragend={handleDragEnd}
                        on:keydown={(e) => {
            if ((e.key === 'Enter' || e.key === ' ') && interactive && fileObj) {
                e.preventDefault();
                // Handle keyboard activation (same as click)
                console.log('File activated via keyboard:', getFileName(fileObj));
            }
        }}
                        role="button"
                        tabindex={interactive && fileObj ? 0 : -1}
                        aria-label={`Audio file ${index + 1}: ${getFileName(fileObj)}`}
                >
                    <!-- File uploaded state -->
                    <div class="file-content">
                        {#if interactive}
                            <button
                                    class="remove-button"
                                    on:click={() => removeFile(index)}
                                    aria-label="Remove audio file"
                            >
                                ×
                            </button>
                        {/if}

                        <div class="audio-icon">
                            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
                            </svg>
                        </div>

                        <div class="file-info">
                            <div class="file-name">{getFileName(fileObj)}</div>
                            {#if interactive}
                                <div class="drag-handle" role="img" aria-label="Drag handle">
                                    <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
                                        <circle cx="3" cy="3" r="1"/>
                                        <circle cx="9" cy="3" r="1"/>
                                        <circle cx="3" cy="6" r="1"/>
                                        <circle cx="9" cy="6" r="1"/>
                                        <circle cx="3" cy="9" r="1"/>
                                        <circle cx="9" cy="9" r="1"/>
                                    </svg>
                                </div>
                            {/if}
                        </div>
                    </div>
                </div>
            {/each}

            <!-- Always show one empty upload slot when interactive and under max files -->
            {#if interactive}
                <div class="upload-square">
                    <div
                            class="upload-zone"
                            role="button"
                            tabindex="0"
                            aria-label="Upload audio file"
                            on:dragover={handleDragOver}
                            on:drop={(e) => handleFileDrop(e)}
                    >
                        <input
                                type="file"
                                accept="audio/*"
                                class="file-input"
                                bind:this={fileInputs[value.length]}
                                on:change={(e) => handleFileChange(e)}
                        />

                        <button
                                type="button"
                                class="upload-content"
                                on:click={() => fileInputs[value.length]?.click()}
                                on:keydown={(e) => {
                                    if (e.key === 'Enter' || e.key === ' ') {
                                        e.preventDefault();
                                        fileInputs[value.length]?.click();
                                    }
                                }}
                        >
                            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                 stroke-width="2">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                                <polyline points="7,10 12,15 17,10"/>
                                <line x1="12" y1="15" x2="12" y2="3"/>
                            </svg>
                            <div class="upload-text">
                                <div>Drop audio file</div>
                                <div class="upload-subtext">or click to browse</div>
                            </div>
                        </button>
                    </div>
                </div>
            {/if}

            {#if value.length === 0}
                <div class="empty-state" role="status" aria-live="polite">
                    {interactive ? "Drag & drop audio files or click to browse" : "No audio files"}
                </div>
            {/if}
        </div>
    </div>
</Block>

<style>
    .audio-upload-container {
        width: 100%;
    }

    .upload-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        align-content: flex-start;
        min-height: 160px;
        position: relative;
    }

    .upload-square {
        width: 140px;
        height: 140px;
        border: 2px dashed var(--input-border-color);
        border-radius: var(--input-radius);
        background: var(--background-fill-secondary);
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }

    .upload-square.has-file {
        border: 1px solid var(--border-color-primary);
        background: var(--background-fill-primary);
        cursor: grab;
    }

    .upload-square.dragging {
        opacity: 0.5;
        transform: rotate(2deg);
        cursor: grabbing;
    }

    .upload-square:hover {
        border-color: var(--border-color-accent);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .upload-zone {
        width: 100%;
        height: 100%;
        position: relative;
        cursor: pointer;
    }

    .file-input {
        position: absolute;
        width: 100%;
        height: 100%;
        opacity: 0;
        cursor: pointer;
    }

    .upload-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        padding: 16px;
        text-align: center;
        color: var(--body-text-color-subdued);
        transition: color 0.2s;
        border: none;
        background: none;
        cursor: pointer;
        gap: 8px;
    }

    .upload-content:hover {
        color: var(--body-text-color);
    }

    .upload-text {
        font-size: var(--text-sm);
    }

    .upload-subtext {
        font-size: var(--text-xs);
        opacity: 0.7;
        margin-top: 4px;
    }

    .file-content {
        display: flex;
        flex-direction: column;
        height: 100%;
        padding: 12px;
        position: relative;
    }

    .remove-button {
        position: absolute;
        top: 8px;
        right: 8px;
        background: var(--background-fill-primary);
        border: 1px solid var(--border-color-primary);
        color: var(--body-text-color-subdued);
        cursor: pointer;
        font-size: 14px;
        line-height: 1;
        padding: 4px;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
        z-index: 10;
    }

    .remove-button:hover {
        background: var(--color-accent);
        color: white;
    }

    .audio-icon {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--color-accent);
    }

    .file-info {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
    }

    .file-name {
        font-size: var(--text-xs);
        color: var(--body-text-color);
        text-align: center;
        word-break: break-word;
        line-height: 1.2;
        max-height: 2.4em;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .drag-handle {
        color: var(--body-text-color-subdued);
        cursor: grab;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 4px;
        border-radius: 4px;
        transition: background-color 0.2s;
    }

    .drag-handle:hover {
        background: var(--background-fill-secondary);
    }

    .empty-state {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: var(--body-text-color-subdued);
        font-style: italic;
        padding: 20px;
        pointer-events: none;
        z-index: 1;
    }

    /* Mobile/Tablet responsive styles */
    @media (max-width: 768px) {
        .upload-grid {
            justify-content: center;
        }

        .audio-upload-container {
            text-align: center;
        }

        .upload-square {
            width: 120px;
            height: 120px;
        }
    }

    /* Non-interactive styles */
    .upload-square:not(.has-file) {
        cursor: default;
    }

    .upload-square:not([draggable="true"]) .drag-handle {
        display: none;
    }
</style>