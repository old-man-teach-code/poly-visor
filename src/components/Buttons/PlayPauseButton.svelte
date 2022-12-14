<script>
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	let color;
	function handleEvent() {
		color = !color;
		dispatch('event');
	}
</script>

<button on:click={handleEvent}>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		fill="none"
		viewBox="0 0 24 24"
		stroke-width="1.5"
		stroke="currentColor"
		class="w-16 h-16 hover:text-orange-400 {color ? 'text-green-400' : 'text-red-400'}"
	>
		<path
			stroke-linecap="round"
			stroke-linejoin="round"
			d="M21 7.5V18M15 7.5V18M3 16.811V8.69c0-.864.933-1.406 1.683-.977l7.108 4.061a1.125 1.125 0 010 1.954l-7.108 4.061A1.125 1.125 0 013 16.811z"
		/>
	</svg>
</button>
