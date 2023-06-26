<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	export let direction: string;
	export function handleEvent() {
		dispatch('event');
	}

	let arrow = {
		right: 'M8.25 4.5l7.5 7.5-7.5 7.5',
		left: 'M15.75 19.5L8.25 12l7.5-7.5',
		down: 'M19.5 8.25l-7.5 7.5-7.5-7.5',
		up: 'M4.5 15.75l7.5-7.5 7.5 7.5'
	};
</script>

<button on:click={handleEvent}>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		fill="none"
		viewBox="0 0 24 24"
		stroke-width="1.5"
		stroke="currentColor"
		class="w-8 h-8 text-orange-400"
	>
		<path stroke-linecap="round" stroke-linejoin="round" d={arrow[direction]} />
	</svg>
</button>
