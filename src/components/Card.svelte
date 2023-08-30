<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	function handleEvent() {
		dispatch('event');
	}
	export let enabled : Boolean = false;
	export let content:any;
	export let title:string;
</script>

<button
	class="sm:hover:text-2xl border-2 bg-white w-full h-32 max-md:h-24 rounded-md min-h-fit {enabled? 'text-[#FF8C32] shadow-slate-300 shadow-lg': 'text-black'}"
	on:click={handleEvent}
>
	<h1 class="text-xl">{title}</h1>
	<h4>{content}</h4>
</button>
