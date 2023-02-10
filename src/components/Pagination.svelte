<script>
	import ArrowButton from './Buttons/ArrowButton.svelte';
	export let rows;
	export let perPage;
	export let trimmedRows;
	export let currentPage;

	$: totalRows = rows.length;
	$: currentPage = 0;
	$: totalPages = Math.ceil(totalRows / perPage);
	$: start = currentPage * perPage;
	$: end = currentPage === totalPages - 1 ? totalRows - 1 : start + perPage - 1;

	$: trimmedRows = rows.slice(start, end + 1);

	$: totalRows, (currentPage = 0);
	$: currentPage, start, end;
</script>

{#if totalRows && totalRows > perPage}
	<div class="flex justify-center">
		{#if currentPage > 0}
			<div class="absolute mr-52">
				<ArrowButton direction="left" on:event={() => (currentPage -= 1)} />
			</div>
		{/if}

		<span class="sr-only">Load previous {perPage} rows</span>
		<p class="px-52">{start + 1} - {end + 1} of {totalRows}</p>
		{#if currentPage < totalPages - 1}
			<div class="absolute ml-52">
				<ArrowButton direction="right" on:event={() => (currentPage += 1)} />
			</div>
		{/if}
		<span class="sr-only">Load next {perPage} rows</span>
	</div>
{/if}
