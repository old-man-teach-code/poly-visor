<script>
	export let coreName;
	export let coreValue;

	let coreColor;
	$: if (coreValue < 30.0) {
		coreColor = 'bg-green-300';
	} else if (coreValue < 50) {
		coreColor = 'bg-yellow-300';
	} else {
		coreColor = 'bg-red-300';
	}
</script>

<div class="flex justify-center items-center border-2 bg-white w-28 h-28 {coreColor} rounded-full">
	<div class="w-fit h-fit text-center">
		<p>Core {coreName}</p>
		<p>{coreValue}%</p>
	</div>
</div>
