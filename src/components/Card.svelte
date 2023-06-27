<script>
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	function handleEvent() {
		dispatch('event');
	}
	export let color;
	export let content;
	export let title;
</script>

<button
	class="sm:hover:text-2xl border-2 bg-white w-full h-32 max-md:h-24 rounded-md min-h-fit {color}"
	on:click={handleEvent}
>
	<h1 class="text-xl">{title}</h1>
	<h4>{content}</h4>
</button>
