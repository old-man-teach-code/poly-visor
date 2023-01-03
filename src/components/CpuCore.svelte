<script>
	export let coreName;
	export let coreValue;

	let coreColor;
	if (coreValue < 30.0) {
		coreColor = 'bg-green-300';
	} else if (coreValue < 50) {
		coreColor = 'bg-yellow-300';
	} else {
		coreColor = 'bg-red-300';
	}
</script>

<div class="border-2 bg-white w-28 h-28 grid place-content-center {coreColor} rounded-full">
	<div>Core {coreName}</div>
	<div>{coreValue}%</div>
</div>
