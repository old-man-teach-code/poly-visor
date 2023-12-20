<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	function handleEvent() {
		dispatch('event');
	}
	export let enabled: Boolean = false;
	export let content: any;
	export let title: string;
</script>

<button
	class=" w-full border-2 hover:scale-110 bg-white lg:px-8 px-4 py-3 lg:py-6 items-center rounded-md font-bold flex flex-col gap-3 {enabled
		? 'text-[#FF8C32] shadow-slate-300 shadow-lg'
		: ''}"
	on:click={handleEvent}
>
	<h1 class="text-sm sm:text-lg text-[#9FA2B4]">{title}</h1>
	<span class="text-xl sm:text-3xl">{content}</span>
</button>
