<script>
	import { page } from '$app/stores';
	$: pathname = $page.url.pathname;
</script>

<!-- Side bar -->
<div class="bg-sidebar z-50 fixed w-full sm:w-fit max-sm:bottom-0 sm:static">
	<div class="sticky top-0 flex flex-col max-sm:flex-row">
		<div class="hidden sm:flex justify-center items-center gap-2 sm:mx-14 my-8">
			<img class="w-8 h-8" src="/images/logo.png" alt="" />
			<h1 class="text-text-logo text-xl whitespace-nowrap">Poly-Visor</h1>
		</div>
		<ul class="flex sm:flex-col flex-row ">
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
