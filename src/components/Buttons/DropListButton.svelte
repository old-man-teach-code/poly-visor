<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	export let direction: string;
	export function handleEvent() {
		dispatch('event');
	}

	let arrow :any = {
		down: 'M3 4.5h14.25M3 9h9.75M3 13.5h9.75m4.5-4.5v12m0 0l-3.75-3.75M17.25 21L21 17.25',
		up: 'M3 4.5h14.25M3 9h9.75M3 13.5h5.25m5.25-.75L17.25 9m0 0L21 12.75M17.25 9v12'
	};
</script>

<button on:click={handleEvent}>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		fill="none"
		viewBox="0 0 24 24"
		stroke-width="1.5"
		stroke="currentColor"
		class="w-6 h-6 text-orange-400"
	>
		<path stroke-linecap="round" stroke-linejoin="round" d={arrow[direction]} />
	</svg>
</button>
