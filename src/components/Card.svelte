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
	class="hover:text-2xl border-2 bg-white w-full h-32 rounded-md {color}"
	on:click={handleEvent}
>
	<h1 class="text-xl">{title}</h1>
	<h4>{content}</h4>
</button>
