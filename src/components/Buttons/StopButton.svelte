<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	export let spin: Boolean;
	function handleEvent() {
		dispatch('event');
	}
</script>

{#if spin}
	<button on:click={handleEvent}>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			stroke-width="1.5"
			stroke="currentColor"
			class="text-red-400 hover:text-orange-400 w-6 h-6"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				d="M5.25 7.5A2.25 2.25 0 017.5 5.25h9a2.25 2.25 0 012.25 2.25v9a2.25 2.25 0 01-2.25 2.25h-9a2.25 2.25 0 01-2.25-2.25v-9z"
			/>
		</svg>
		<slot />
	</button>
{:else}
	<button on:click={handleEvent}>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			stroke-width="1.5"
			stroke="currentColor"
			class="text-red-400 hover:text-orange-400 w-8 h-8"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				d="M5.25 7.5A2.25 2.25 0 017.5 5.25h9a2.25 2.25 0 012.25 2.25v9a2.25 2.25 0 01-2.25 2.25h-9a2.25 2.25 0 01-2.25-2.25v-9z"
			/>
		</svg>
		<slot />
	</button>
{/if}
