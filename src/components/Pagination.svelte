<script>
	export let rows;
	export let perPage;
	export let trimmedRows;

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
	<div class="flex pt-20 justify-center">
		<button
			on:click={() => (currentPage -= 1)}
			disabled={currentPage === 0 ? true : false}
			aria-label="left arrow icon"
			aria-describedby="prev"
		>
			Prev
		</button>
		<span class="sr-only">Load previous {perPage} rows</span>
		<p class="px-52">{start + 1} - {end + 1} of {totalRows}</p>
		<button
			on:click={() => (currentPage += 1)}
			disabled={currentPage === totalPages - 1 ? true : false}
			aria-label="right arrow icon"
			aria-describedby="next"
		>
			Next</button
		>
		<span class="sr-only">Load next {perPage} rows</span>
	</div>
{/if}
