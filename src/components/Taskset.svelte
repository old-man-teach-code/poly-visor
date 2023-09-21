<script lang="ts">
	import { onMount } from 'svelte';
	import { Taskset } from '../store/action';

	export let totalCore: any;
	export let process: any;
	let originEnabled = process.core_index;
	let enabled = process.core_index;
	//turn enabled from [1,2,3,4] to "1,2,3,4"
</script>

<div class="flex items-center justify-center flex-col">
	<div class="grid grid-cols-4 gap-6 items-center justify-center place-items-center w-full p-10">
		{#each Object.entries(totalCore) as [key, value]}
			<div
				class="border border-gray-50 bg-slate-100 rounded-full flex flex-row items-center justify-center w-fit"
			>
				<span class="pl-2 pr-1.5">
					{key}
				</span>
				<button
					on:click={() => {
						enabled.includes(parseInt(key))
							? (enabled = enabled.filter((item) => item !== parseInt(key)))
							: (enabled = [...enabled, parseInt(key)]);
						process.core_index = enabled;
					}}
					type="button"
					class="{enabled.includes(parseInt(key)) ? 'bg-green-200' : 'bg-red-200'}
					inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out "
					role="switch"
					aria-checked="false"
				>
					<!-- Enabled: "translate-x-5", Not Enabled: "translate-x-0" -->
					<span
						aria-hidden="true"
						class="
						{enabled.includes(parseInt(key)) ? 'translate-x-5' : 'translate-x-0'}
						pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
					/>
				</button>
			</div>
		{/each}
	</div>
	<button
		class="mb-10 bg-green-200 rounded px-3 py-1"
		on:click={() => {
			if (enabled != originEnabled && enabled.length > 0) {
				enabled = enabled.join(',');
				Taskset(process.pid, enabled);
			}
		}}>Set</button
	>
</div>
