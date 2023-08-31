<script lang="ts">
	export let cores: any;
	export let coreCount: any;

	let show: boolean = false;
</script>

<button
	on:click={() => {
		show = !show;
	}}
	class="bg-green-300 rounded-md px-3 py-1.5"
	>{cores ? cores.length : 0} / {Object.keys(coreCount).length}</button
>
<div
	class="bg-white absolute w-full h-full z-[99] {show
		? 'block'
		: 'hidden'} border border-slate-400 rounded p-4"
>
	<div class="flex flex-wrap gap-2 items-center justify-center w-fit px-2 py-1">
		{#each Object.entries(coreCount) as [key, value]}
			<button class="bg-green-200">{key}</button>
		{/each}
	</div>
</div>
