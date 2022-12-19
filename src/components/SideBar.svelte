<script>
	import { page } from '$app/stores';
	let overview;
	let processes;
	let setting;
	$: if ($page.url.pathname == '/') {
		overview = true;
		processes = false;
		setting = false;
	} else if ($page.url.pathname == '/processes') {
		processes = true;
		overview = false;
		setting = false;
	} else {
		setting = true;
		overview = false;
		processes = false;
	}
</script>

<!-- Side bar -->
<div class="bg-sidebar w-56 h-screen fixed overflow-auto">
	<div class="inline-flex justify-center py-5 w-full">
		<img class="w-8 h-8" src="src/images/logo.png" alt="" />
		<h1 class="ml-3 text-text-logo text-xl">Poly-Visor</h1>
	</div>
	<ul class="pt-5">
		<li class="text-center">
			<a
				href="/"
				class="text-white text-sm py-5 pr-8 justify-center flex hover:bg-gray-600 {overview
					? 'bg-gray-600'
					: 'bg-sidebar'}"
				><img class="mr-2 w-5 h-5" src="src/images/graph.png" alt="" />
				<p>Overview</p>
			</a>
		</li>
		<li>
			<a
				href="/processes"
				class="text-white text-sm pr-8 justify-center py-5 flex hover:bg-gray-600 {processes
					? 'bg-gray-600'
					: 'bg-sidebar'}"
				><img class=" mr-2 w-5 h-5" src="src/images/process.png" alt="" />Processes</a
			>
		</li>
	</ul>
	<div class="h-px bg-gray-600 mt-48" />
	<div>
		<a
			href="#setting"
			class="text-white justify-center pr-14 text-sm py-5 flex hover:bg-gray-600 {setting
				? 'bg-gray-600'
				: 'bg-sidebar'}}"
			><img class=" mr-2 w-5 h-5" src="src/images/setting.png" alt="" />Setting</a
		>
	</div>
</div>
