<script lang="ts">
	import { onMount } from 'svelte';

	export let title: String;
	let tooltip: String;
	onMount(() => {
		tooltip = 'invisible';
	});
	function handleMouseOver(e) {
		tooltip = 'visible';
	}
	function handleMouseOut(e) {
		tooltip = 'invisible';
	}
</script>

<div>
	<div on:mouseover={handleMouseOver} on:mouseout={handleMouseOut} class="flex flex-wrap">
		<slot />
	</div>
	<span
		class="{tooltip} absolute text-center border border-solid border-gray-300 shadow-sm bg-white rounded px-1 text-gray-600 z-[1]"
		>{title}</span
	>
</div>
