<script>
	import { page } from '$app/stores';
	$: pathname = $page.url.pathname;
</script>

<!-- Side bar -->
<div class="bg-sidebar sm:w-56 sm:h-screen max-sm:bottom-0 max-sm:w-full fixed overflow-auto z-50 ">
	<div class="flex flex-col max-sm:flex-row">
		<div class="inline-flex justify-center py-5 sm:w-full max-sm:hidden">
			<img class="w-8 h-8" src="/images/logo.png" alt="" />
			<h1 class="ml-3 text-text-logo text-xl">Poly-Visor</h1>
		</div>
		<ul class="sm:pt-5 flex flex-col max-sm:flex-row ">
			<li class="text-center">
				<a
					href="/"
					class="text-white text-sm py-5 max-sm:px-5 justify-center flex hover:bg-gray-600 {pathname ==
					'/'
						? 'bg-gray-600'
						: 'bg-sidebar'}"
					><img class="mr-2 w-5 h-5" src="/images/graph.png" alt="" />
					<p class="max-sm:hidden">Overview</p>
				</a>
			</li>
			<li>
				<a
					href="/processes"
					class="text-white text-sm justify-center py-5 max-sm:px-5  flex hover:bg-gray-600 {pathname ==
					'/processes'
						? 'bg-gray-600'
						: 'bg-sidebar'}"
					><img class=" mr-2 w-5 h-5 " src="/images/process.png" alt="" />
					<p class="max-sm:hidden">Processes</p></a
				>
			</li>
		</ul>
	</div>
</div>
