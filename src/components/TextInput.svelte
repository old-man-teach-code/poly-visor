<script lang="ts">
	export let inputLabel: string;
	export let inputPlaceholder: string;
	export let inputValue: string;
</script>

<div>
	{#if inputLabel}
		<label for="text" class="block text-sm font-medium text-gray-700">{inputLabel}</label>
	{/if}
	<div class="mt-1">
		<input
			bind:value={inputValue}
			type="text"
			name="text"
			id="text"
			class="block w-full rounded-md border-gray-300 shadow-sm focus:border-orange-500 focus:ring-orange-500 sm:text-sm"
			placeholder={inputPlaceholder}
		/>
	</div>
</div>
