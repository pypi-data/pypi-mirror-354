<script lang="ts">
    import type { LoadingStatus } from "@gradio/statustracker";
    import type { Gradio } from "@gradio/utils";
    import { onMount } from 'svelte';
    
    export let gradio: Gradio<{
        change: never;
        input: never;
    }>;
    export let elem_id = "";
    export const elem_classes: string[] = [];
    export let value: any = { components: [], layout: "blocks" };
    export const loading_status: LoadingStatus | undefined = undefined;
    export const mode: "static" | "interactive" = "interactive";

    // Complete component definitions organized by category
    const componentsByCategory = {
        "Input": [
            { type: "Textbox", label: "Text Input", icon: "📝" },
            { type: "TextArea", label: "Text Area", icon: "📄" },
            { type: "Number", label: "Number", icon: "🔢" },
            { type: "Slider", label: "Slider", icon: "🎚️" },
            { type: "Checkbox", label: "Checkbox", icon: "☑️" },
            { type: "CheckboxGroup", label: "Checkbox Group", icon: "☑️" },
            { type: "Radio", label: "Radio", icon: "🔘" },
            { type: "Dropdown", label: "Dropdown", icon: "📋" },
            { type: "Toggle", label: "Toggle", icon: "🔄" },
            { type: "ColorPicker", label: "Color Picker", icon: "🎨" },
            { type: "Date", label: "Date", icon: "📅" },
            { type: "Time", label: "Time", icon: "⏰" },
            { type: "File", label: "File Upload", icon: "📁" }
        ],
        "Action": [
            { type: "Button", label: "Button", icon: "🔘" }
        ],
        "Media": [
            { type: "Image", label: "Image", icon: "🖼️" },
            { type: "Video", label: "Video", icon: "🎥" },
            { type: "Audio", label: "Audio", icon: "🎵" }
        ],
        "Data": [
            { type: "Dataframe", label: "Dataframe", icon: "📊" },
            { type: "JSON", label: "JSON", icon: "📋" }
        ],
        "Display": [
            { type: "Markdown", label: "Markdown", icon: "📝" },
            { type: "HTML", label: "HTML", icon: "🌐" },
            { type: "Label", label: "Label", icon: "🏷️" },
            { type: "Progress", label: "Progress", icon: "📈" }
        ]
    };

    // Force components to show immediately on mount
    let mounted = false;
    onMount(() => {
        mounted = true;
    });

    let draggedComponent: any = null;
    let canvasRef: HTMLElement;
    let selectedComponent: any = null;
    let searchFilter = "";
    let selectedCategory = "All";

    // Ensure components are always available
    $: allComponents = Object.values(componentsByCategory).flat();
    
    $: filteredComponents = (() => {
        if (selectedCategory === "All") {
            let components = allComponents;
            
            if (searchFilter.trim()) {
                return components.filter(comp => 
                    comp.type.toLowerCase().includes(searchFilter.toLowerCase()) ||
                    comp.label.toLowerCase().includes(searchFilter.toLowerCase())
                );
            }
            
            return components;
        } else {
            let components = componentsByCategory[selectedCategory] || [];
            
            if (searchFilter.trim()) {
                return components.filter(comp => 
                    comp.type.toLowerCase().includes(searchFilter.toLowerCase()) ||
                    comp.label.toLowerCase().includes(searchFilter.toLowerCase())
                );
            }
            
            return components;
        }
    })();
    
    // Use this to display components on initial load
    $: displayComponents = mounted ? filteredComponents : allComponents;

    function onDragStart(event: DragEvent, componentType: any) {
        draggedComponent = componentType;
        if (event.dataTransfer) {
            event.dataTransfer.effectAllowed = "copy";
        }
    }

    function onDragOver(event: DragEvent) {
        event.preventDefault();
        if (event.dataTransfer) {
            event.dataTransfer.dropEffect = "copy";
        }
    }

    function onDrop(event: DragEvent) {
        event.preventDefault();
        if (!draggedComponent) return;

        const rect = canvasRef.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        const newComponent = {
            id: `${draggedComponent.type.toLowerCase()}_${Date.now()}`,
            type: draggedComponent.type,
            position: { x, y },
            size: { width: 200, height: 100 },
            props: getDefaultProps(draggedComponent.type)
        };

        value = {
            ...value,
            components: [...value.components, newComponent]
        };

        gradio.dispatch("change", value);
        draggedComponent = null;
    }

    function getDefaultProps(type: string) {
        const defaults = {
            Textbox: { label: "Text Input", placeholder: "Enter text...", value: "" },
            TextArea: { label: "Text Area", placeholder: "Enter multiple lines...", lines: 3, value: "" },
            Button: { value: "Click me", variant: "secondary", size: "sm" },
            Slider: { label: "Slider", minimum: 0, maximum: 100, step: 1, value: 50 },
            Number: { label: "Number", value: 0, precision: 0 },
            Checkbox: { label: "Checkbox", value: false },
            CheckboxGroup: { label: "Checkbox Group", choices: ["Option 1", "Option 2"], value: [] },
            Radio: { label: "Radio", choices: ["Option 1", "Option 2"], value: "Option 1" },
            Dropdown: { label: "Dropdown", choices: ["Option 1", "Option 2"], value: "Option 1", multiselect: false },
            Toggle: { label: "Toggle", value: false },
            ColorPicker: { label: "Color Picker", value: "#ff0000" },
            Date: { label: "Date", value: "2025-01-01" },
            Time: { label: "Time", value: "12:00" },
            File: { label: "Upload File", file_types: [".txt", ".pdf"] },
            Image: { label: "Image", type: "pil", interactive: true },
            Video: { label: "Video", format: "mp4" },
            Audio: { label: "Audio" },
            Dataframe: { headers: ["Column 1", "Column 2"], datatype: ["str", "str"], value: [] },
            JSON: { value: "{}" },
            Markdown: { value: "# Markdown Text" },
            HTML: { value: "<p>HTML Content</p>" },
            Label: { value: "Label Text" },
            Progress: { value: 0.5 }
        };
        return defaults[type] || {};
    }

    function selectComponent(component: any) {
        selectedComponent = component;
    }

    function updateComponentProp(prop: string, newValue: any) {
        if (!selectedComponent) return;
        
        // Handle special input types
        if (prop === "choices" && typeof newValue === "string") {
            newValue = newValue.split(",").map(s => s.trim()).filter(s => s);
        } else if (prop === "file_types" && typeof newValue === "string") {
            newValue = newValue.split(",").map(s => s.trim()).filter(s => s);
        }
        
        const updatedComponents = value.components.map(comp => 
            comp.id === selectedComponent.id 
                ? { ...comp, props: { ...comp.props, [prop]: newValue }}
                : comp
        );
        
        selectedComponent = { ...selectedComponent, props: { ...selectedComponent.props, [prop]: newValue }};
        value = { ...value, components: updatedComponents };
        gradio.dispatch("change", value);
    }

    function updateComponentPosition(component: any, newX: number, newY: number) {
        const updatedComponents = value.components.map(comp => 
            comp.id === component.id 
                ? { ...comp, position: { x: newX, y: newY }}
                : comp
        );
        
        value = { ...value, components: updatedComponents };
        gradio.dispatch("change", value);
    }

    function updateComponentSize(component: any, newWidth: number, newHeight: number) {
        const updatedComponents = value.components.map(comp => 
            comp.id === component.id 
                ? { ...comp, size: { width: newWidth, height: newHeight }}
                : comp
        );
        
        if (selectedComponent?.id === component.id) {
            selectedComponent = { ...selectedComponent, size: { width: newWidth, height: newHeight }};
        }
        
        value = { ...value, components: updatedComponents };
        gradio.dispatch("change", value);
    }

    function deleteComponent(componentId: string) {
        const updatedComponents = value.components.filter(comp => comp.id !== componentId);
        value = { ...value, components: updatedComponents };
        selectedComponent = null;
        gradio.dispatch("change", value);
    }

    function exportAsJSON() {
        const exportData = {
            ...value,
            metadata: {
                version: "1.0",
                created_at: new Date().toISOString(),
                app_type: "gradio_interface",
                component_count: value.components.length
            }
        };
        
        const jsonString = JSON.stringify(exportData, null, 2);
        const blob = new Blob([jsonString], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'gradio-design.json';
        a.click();
        URL.revokeObjectURL(url);
    }

    function exportAsPNG() {
        try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            const rect = canvasRef.getBoundingClientRect();
            canvas.width = rect.width * 2;
            canvas.height = rect.height * 2;
            
            ctx.scale(2, 2);
            
            // White background
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, rect.width, rect.height);
            
            // Draw grid
            ctx.strokeStyle = 'rgba(0,0,0,0.1)';
            ctx.lineWidth = 1;
            for (let x = 0; x <= rect.width; x += 20) {
                ctx.moveTo(x, 0);
                ctx.lineTo(x, rect.height);
            }
            for (let y = 0; y <= rect.height; y += 20) {
                ctx.moveTo(0, y);
                ctx.lineTo(rect.width, y);
            }
            ctx.stroke();
            
            // Draw components
            value.components.forEach(component => {
                const componentDef = allComponents.find(c => c.type === component.type);
                
                ctx.fillStyle = '#ffffff';
                ctx.strokeStyle = '#ddd';
                ctx.lineWidth = 2;
                
                ctx.fillRect(component.position.x, component.position.y, component.size.width, component.size.height);
                ctx.strokeRect(component.position.x, component.position.y, component.size.width, component.size.height);
                
                // Component icon and text
                ctx.fillStyle = '#333';
                ctx.font = '16px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(
                    componentDef?.icon || '📦', 
                    component.position.x + component.size.width/2, 
                    component.position.y + 25
                );
                
                ctx.font = '12px Arial';
                ctx.fillText(
                    component.type, 
                    component.position.x + component.size.width/2, 
                    component.position.y + component.size.height/2
                );
                
                ctx.fillText(
                    component.props.label || component.props.value || '', 
                    component.position.x + component.size.width/2, 
                    component.position.y + component.size.height/2 + 15
                );
            });
            
            const link = document.createElement('a');
            link.download = 'gradio-design.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
            
        } catch (error) {
            console.error('Canvas export failed:', error);
            alert('PNG export failed. Check console for details.');
        }
    }

    // Make components draggable within canvas
    let isDragging = false;
    let dragOffset = { x: 0, y: 0 };

    function onComponentMouseDown(event: MouseEvent, component: any) {
        if (event.button !== 0) return; // Only left click
        
        isDragging = true;
        selectedComponent = component;
        
        const rect = canvasRef.getBoundingClientRect();
        dragOffset.x = event.clientX - rect.left - component.position.x;
        dragOffset.y = event.clientY - rect.top - component.position.y;
        
        event.preventDefault();
    }

    function onCanvasMouseMove(event: MouseEvent) {
        if (!isDragging || !selectedComponent) return;
        
        const rect = canvasRef.getBoundingClientRect();
        const newX = event.clientX - rect.left - dragOffset.x;
        const newY = event.clientY - rect.top - dragOffset.y;
        
        updateComponentPosition(selectedComponent, Math.max(0, newX), Math.max(0, newY));
    }

    function onCanvasMouseUp() {
        isDragging = false;
    }
</script>

<svelte:window on:mousemove={onCanvasMouseMove} on:mouseup={onCanvasMouseUp} />

<div class="designer-container" id={elem_id}>
    <!-- Top Toolbar -->
    <div class="toolbar">
        <div class="toolbar-left">
            <h3>🎨 Gradio Designer</h3>
            <span class="component-count">{value.components.length} components</span>
        </div>
        <div class="toolbar-right">
            <button class="export-btn" on:click={exportAsJSON} type="button">
                📄 Export JSON
            </button>
            <button class="export-btn" on:click={exportAsPNG} type="button">
                🖼️ Export PNG
            </button>
        </div>
    </div>

    <div class="designer-content">
        <!-- Component Palette - Always on the left -->
        <div class="palette">
            <div class="palette-header">
                <h4>Components</h4>
                <input 
                    type="text" 
                    placeholder="Search components..." 
                    bind:value={searchFilter}
                    class="search-input"
                />
                <select bind:value={selectedCategory} class="category-select">
                    <option value="All">All Categories</option>
                    {#each Object.keys(componentsByCategory) as category}
                        <option value={category}>{category}</option>
                    {/each}
                </select>
            </div>
            
            <div class="palette-content">
                {#each displayComponents as component}
                    <div 
                        class="palette-item"
                        draggable="true"
                        on:dragstart={(e) => onDragStart(e, component)}
                    >
                        <span class="icon">{component.icon}</span>
                        <span class="label">{component.label}</span>
                    </div>
                {:else}
                    <div class="no-components">
                        {#if searchFilter.trim()}
                            No components match "{searchFilter}"
                        {:else}
                            Loading components...
                        {/if}
                    </div>
                {/each}
            </div>
        </div>

        <!-- Design Canvas -->
        <div 
            class="canvas"
            bind:this={canvasRef}
            on:dragover={onDragOver}
            on:drop={onDrop}
        >
            <div class="canvas-grid"></div>
            {#each value.components as component (component.id)}
                <div 
                    class="canvas-component"
                    class:selected={selectedComponent?.id === component.id}
                    style="
                        left: {component.position.x}px; 
                        top: {component.position.y}px;
                        width: {component.size.width}px;
                        height: {component.size.height}px;
                    "
                    on:click={() => selectComponent(component)}
                    on:mousedown={(e) => onComponentMouseDown(e, component)}
                >
                    <div class="component-preview">
                        <div class="component-header">
                            <span class="type">{component.type}</span>
                            <button 
                                class="delete-btn" 
                                on:click|stopPropagation={() => deleteComponent(component.id)}
                                type="button"
                            >
                                ❌
                            </button>
                        </div>
                        <span class="label">{component.props.label || component.props.value || 'Component'}</span>
                    </div>
                </div>
            {/each}
        </div>

        <!-- Properties Panel -->
        <div class="properties">
            <h4>Properties</h4>
            {#if selectedComponent}
                <div class="property-group">
                    <div class="property-header">
                        <strong>Type:</strong> {selectedComponent.type}
                        <br>
                        <small>ID: {selectedComponent.id}</small>
                    </div>
                    
                    <!-- Component Properties -->
                    {#if selectedComponent.props.label !== undefined}
                        <label>Label:</label>
                        <input 
                            type="text" 
                            placeholder="Label"
                            value={selectedComponent.props.label}
                            on:input={(e) => updateComponentProp('label', e.target.value)}
                        />
                    {/if}
                    
                    {#if selectedComponent.props.placeholder !== undefined}
                        <label>Placeholder:</label>
                        <input 
                            type="text" 
                            placeholder="Placeholder"
                            value={selectedComponent.props.placeholder}
                            on:input={(e) => updateComponentProp('placeholder', e.target.value)}
                        />
                    {/if}
                    
                    {#if selectedComponent.props.value !== undefined}
                        <label>Value:</label>
                        {#if typeof selectedComponent.props.value === 'boolean'}
                            <input 
                                type="checkbox" 
                                checked={selectedComponent.props.value}
                                on:change={(e) => updateComponentProp('value', e.target.checked)}
                            />
                        {:else if typeof selectedComponent.props.value === 'number'}
                            <input 
                                type="number" 
                                value={selectedComponent.props.value}
                                on:input={(e) => updateComponentProp('value', parseFloat(e.target.value) || 0)}
                            />
                        {:else}
                            <input 
                                type="text" 
                                placeholder="Value"
                                value={selectedComponent.props.value}
                                on:input={(e) => updateComponentProp('value', e.target.value)}
                            />
                        {/if}
                    {/if}
                    
                    {#if selectedComponent.props.choices !== undefined}
                        <label>Choices (comma-separated):</label>
                        <input 
                            type="text" 
                            placeholder="Option 1, Option 2, Option 3"
                            value={Array.isArray(selectedComponent.props.choices) ? selectedComponent.props.choices.join(", ") : selectedComponent.props.choices}
                            on:input={(e) => updateComponentProp('choices', e.target.value)}
                        />
                    {/if}
                    
                    {#if selectedComponent.props.minimum !== undefined}
                        <label>Minimum:</label>
                        <input 
                            type="number" 
                            value={selectedComponent.props.minimum}
                            on:input={(e) => updateComponentProp('minimum', parseFloat(e.target.value) || 0)}
                        />
                    {/if}
                    
                    {#if selectedComponent.props.maximum !== undefined}
                        <label>Maximum:</label>
                        <input 
                            type="number" 
                            value={selectedComponent.props.maximum}
                            on:input={(e) => updateComponentProp('maximum', parseFloat(e.target.value) || 100)}
                        />
                    {/if}
                    
                    {#if selectedComponent.props.step !== undefined}
                        <label>Step:</label>
                        <input 
                            type="number" 
                            value={selectedComponent.props.step}
                            on:input={(e) => updateComponentProp('step', parseFloat(e.target.value) || 1)}
                        />
                    {/if}

                    <!-- Size Controls -->
                    <div class="size-section">
                        <h5>Size & Position</h5>
                        <div class="size-controls">
                            <label>Width:</label>
                            <input 
                                type="number" 
                                value={selectedComponent.size.width}
                                on:input={(e) => updateComponentSize(selectedComponent, parseInt(e.target.value) || 200, selectedComponent.size.height)}
                            />
                            
                            <label>Height:</label>
                            <input 
                                type="number" 
                                value={selectedComponent.size.height}
                                on:input={(e) => updateComponentSize(selectedComponent, selectedComponent.size.width, parseInt(e.target.value) || 100)}
                            />
                            
                            <label>X Position:</label>
                            <input 
                                type="number" 
                                value={selectedComponent.position.x}
                                on:input={(e) => updateComponentPosition(selectedComponent, parseInt(e.target.value) || 0, selectedComponent.position.y)}
                            />
                            
                            <label>Y Position:</label>
                            <input 
                                type="number" 
                                value={selectedComponent.position.y}
                                on:input={(e) => updateComponentPosition(selectedComponent, selectedComponent.position.x, parseInt(e.target.value) || 0)}
                            />
                        </div>
                    </div>
                </div>
            {:else}
                <p>Select a component to edit properties</p>
                <div class="help-text">
                    <strong>How to use:</strong>
                    <ul>
                        <li>Drag components from the palette to the canvas</li>
                        <li>Click components to select and edit them</li>
                        <li>Drag components around the canvas to reposition</li>
                        <li>Use the properties panel to customize</li>
                    </ul>
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
    .designer-container {
        display: flex;
        flex-direction: column;
        height: 700px;
        border: 1px solid #ddd;
        border-radius: 8px;
        overflow: hidden;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 16px;
        background: #f8f9fa;
        border-bottom: 1px solid #ddd;
    }

    .toolbar-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .toolbar h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
    }

    .component-count {
        background: #e9ecef;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        color: #495057;
    }

    .toolbar-right {
        display: flex;
        gap: 8px;
    }

    .export-btn {
        padding: 6px 12px;
        background: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 12px;
    }

    .export-btn:hover {
        background: #0056b3;
    }

    /* CRITICAL FIX: Force grid layout with !important to ensure initial render is correct */
    .designer-content {
        display: grid !important;
        grid-template-columns: 250px 1fr 280px !important;
        grid-template-areas: "palette canvas properties" !important;
        flex: 1;
        height: 100%;
        min-height: 0; /* Force grid to work immediately */
    }

    /* CRITICAL FIX: Use grid-area with !important to lock positions */
    .palette {
        grid-area: palette !important;
        background: #f8f9fa;
        border-right: 1px solid #ddd;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .canvas {
        grid-area: canvas !important;
        position: relative;
        background: white;
        overflow: hidden;
        user-select: none;
    }

    .properties {
        grid-area: properties !important;
        background: #f8f9fa;
        padding: 16px;
        border-left: 1px solid #ddd;
        overflow-y: auto;
    }

    .palette-header {
        padding: 12px 16px;
        border-bottom: 1px solid #ddd;
        background: white;
        flex-shrink: 0;
        min-height: 120px;
        max-height: 120px;
        overflow: hidden;
    }

    .palette h4 {
        margin: 0 0 8px 0;
        font-size: 14px;
        font-weight: 600;
    }

    .search-input, .category-select {
        width: 100%;
        padding: 6px 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 12px;
        margin-bottom: 6px;
        box-sizing: border-box;
    }

    .palette-content {
        flex: 1;
        overflow-y: auto;
        padding: 8px;
        min-height: 0;
        background: #f8f9fa;
    }

    .palette-item {
        display: flex;
        align-items: center;
        padding: 8px;
        margin-bottom: 4px;
        background: white;
        border: 1px solid #e1e5e9;
        border-radius: 4px;
        cursor: grab;
        user-select: none;
    }

    .palette-item:hover {
        background: #f0f0f0;
    }

    .no-components {
        padding: 20px;
        text-align: center;
        color: #666;
        font-size: 12px;
        background: white;
        border-radius: 4px;
        border: 1px solid #e1e5e9;
    }

    .icon {
        margin-right: 8px;
        font-size: 16px;
    }

    .label {
        font-size: 12px;
    }

    .canvas-grid {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            linear-gradient(rgba(0,0,0,0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,0,0,0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        opacity: 0.3;
    }

    .canvas-component {
        position: absolute;
        border: 2px solid #ddd;
        border-radius: 4px;
        background: white;
        cursor: move;
        padding: 8px;
        box-sizing: border-box;
    }

    .canvas-component:hover {
        border-color: #007bff;
    }

    .canvas-component.selected {
        border-color: #ff6b6b;
        box-shadow: 0 0 0 2px rgba(255, 107, 107, 0.3);
    }

    .component-preview {
        display: flex;
        flex-direction: column;
        height: 100%;
        text-align: center;
        pointer-events: none;
    }

    .component-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
    }

    .type {
        font-weight: bold;
        font-size: 12px;
        color: #666;
    }

    .delete-btn {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 10px;
        padding: 2px;
        opacity: 0.7;
        pointer-events: auto;
    }

    .delete-btn:hover {
        opacity: 1;
    }

    .properties h4 {
        margin: 0 0 16px 0;
        font-size: 14px;
        font-weight: 600;
    }

    .property-group {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .property-header {
        padding: 12px;
        background: white;
        border-radius: 4px;
        border: 1px solid #e1e5e9;
        margin-bottom: 12px;
    }

    .size-section {
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px solid #ddd;
    }

    .size-section h5 {
        margin: 0 0 8px 0;
        font-size: 12px;
        font-weight: 600;
    }

    .size-controls {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }

    .property-group label {
        font-size: 12px;
        font-weight: 500;
        color: #333;
    }

    .property-group input, .property-group select {
        padding: 6px 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 12px;
    }

    .help-text {
        margin-top: 20px;
        padding: 12px;
        background: white;
        border-radius: 4px;
        border: 1px solid #e1e5e9;
    }

    .help-text ul {
        margin: 8px 0 0 0;
        padding-left: 16px;
    }

    .help-text li {
        font-size: 11px;
        margin-bottom: 4px;
    }
</style>
