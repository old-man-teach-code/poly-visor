<script>
	import { page } from '$app/stores';
	$: pathname = $page.url.pathname;

	function handleLogout() {
		localStorage.clear();
		window.location.href = '/login';
	}
</script>

<!-- Side bar -->
<div class="bg-sidebar z-50 fixed w-full sm:w-fit max-sm:bottom-0 sm:static">
	<div class="sticky top-0 flex flex-col max-sm:flex-row h-full">
		<div class="hidden sm:flex justify-center items-center gap-2 sm:mx-14 my-8">
			<img class="w-8 h-8" src="/images/logo.png" alt="" />
			<h1 class="text-text-logo text-xl whitespace-nowrap">Poly-Visor</h1>
		</div>
		<div class="flex flex-col justify-between h-2/3 font-bold">
			<ul class="flex sm:flex-col flex-row  ">
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
			<div class="border-t mx-4 border-gray-600">
				<button
					on:click={handleLogout}
					class="text-white text-sm justify-center py-5 max-sm:px-5 gap-2  flex hover:bg-gray-600 w-full"
					><svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 24 24"
						fill="currentColor"
						class="w-6 h-6"
					>
						<path
							fill-rule="evenodd"
							d="M7.5 3.75A1.5 1.5 0 006 5.25v13.5a1.5 1.5 0 001.5 1.5h6a1.5 1.5 0 001.5-1.5V15a.75.75 0 011.5 0v3.75a3 3 0 01-3 3h-6a3 3 0 01-3-3V5.25a3 3 0 013-3h6a3 3 0 013 3V9A.75.75 0 0115 9V5.25a1.5 1.5 0 00-1.5-1.5h-6zm5.03 4.72a.75.75 0 010 1.06l-1.72 1.72h10.94a.75.75 0 010 1.5H10.81l1.72 1.72a.75.75 0 11-1.06 1.06l-3-3a.75.75 0 010-1.06l3-3a.75.75 0 011.06 0z"
							clip-rule="evenodd"
						/>
					</svg>
					Logout</button
				>
			</div>
		</div>
	</div>
</div>
