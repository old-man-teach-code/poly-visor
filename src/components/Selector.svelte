<script>
	import { onMount } from 'svelte';

	export let options;
	export let title;
	let statename = false;
	export let result = [];
	onMount(() => {
		result = options;
	});
</script>

<div class="flex justify-end pr-24 pb-5">
	{#if statename}
		<div
			class="fixed top-0 left-0 w-screen h-screen"
			on:click={() => {
				statename = !statename;
			}}
		/>
	{/if}
	<button
		on:click={() => {
			statename = !statename;
		}}
		type="button"
		class="group inline-flex items-center justify-center text-sm font-medium text-gray-700 hover:text-gray-900"
		aria-expanded="false"
	>
		<span>{title}</span>

		<span
			class="ml-1.5 rounded bg-gray-200 py-0.5 px-1.5 text-xs font-semibold tabular-nums text-gray-700"
			>{result.length}</span
		>
		<!-- Heroicon name: mini/chevron-down -->
		<svg
			class="{statename
				? 'rotate-180'
				: 'rotate-0'} -mr-1 ml-1 h-5 w-5 flex-shrink-0 text-gray-400 group-hover:text-gray-500"
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 20 20"
			fill="currentColor"
			aria-hidden="true"
		>
			<path
				fill-rule="evenodd"
				d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
				clip-rule="evenodd"
			/>
		</svg>
	</button>
	<div
		class="{statename
			? 'transform opacity-100 scale-100 translate-y-5'
			: 'transform opacity-0 scale-95 -translate-x-full'} absolute z-10 mt-2 origin-top-right rounded-md bg-white p-4 shadow-2xl ring-1 ring-black ring-opacity-5 focus:outline-none"
	>
		<form class="space-y-4">
			{#each options as option}
				<div class="flex items-center">
					<input
						bind:group={result}
						id={option}
						name={option}
						value={option}
						type="checkbox"
						class="h-4 w-4 rounded border-gray-300 text-orange-500 focus:ring-orange-400"
					/>
					<label for={option} class="ml-3 whitespace-nowrap pr-6 text-sm font-medium text-gray-900"
						>{option}</label
					>
				</div>
			{/each}
		</form>
	</div>
</div>
