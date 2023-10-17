<script>
	import SideBarButton from './SideBarButton.svelte';
	import OverviewIcon from './OverviewIcon.svelte';
	import ProcessListIcon from './ProcessListIcon.svelte';
	import SettingIcon from './SettingIcon.svelte';
	import LogoutIcon from './LogoutIcon.svelte';
</script>

<!-- Side bar -->
<div class="bg-sidebar z-50 w-full fixed lg:w-fit max-lg:bottom-0 lg:static">
	<div class="sticky top-0 flex lg:flex-col flex-row h-full">
		<div class="hidden lg:flex justify-center items-center gap-2 my-8">
			<img class="w-8 h-8" src="/images/logo.png" alt="" />
			<h1 class="text-text-logo text-xl whitespace-nowrap">Poly-Visor</h1>
		</div>
		<div
			class="flex flex-row lg:flex-col gap-3 justify-between mx-5 lg:mx-0 max-lg:w-full lg:h-2/3 font-bold"
		>
			<ul class="flex lg:flex-col gap-2">
				<li>
					<SideBarButton path="/" text="Overview">
						<OverviewIcon />
					</SideBarButton>
				</li>
				<li>
					<SideBarButton path="/processes" text="Processes">
						<ProcessListIcon />
					</SideBarButton>
				</li>
				<li>
					<!-- <a
						href="/setting"
						class="text-white text-sm justify-center py-5 max-lg:px-5 gap-2 flex hover:bg-gray-600 w-full {pathname ==
						'/processes'
							? 'bg-gray-600'
							: 'bg-sidebar'}"
						><svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="w-6 h-6"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 011.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 01-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.397.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 01-.12-1.45l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.505-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.107-1.204l-.527-.738a1.125 1.125 0 01.12-1.45l.773-.773a1.125 1.125 0 011.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894z"
							/>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
							/>
						</svg>

						<p class="lg:block hidden">Setting</p></a
					> -->
					<SideBarButton path="/setting" text="Setting">
						<SettingIcon />
					</SideBarButton>
				</li>
			</ul>
			<div>
				<div class="border-t hidden lg:block border-gray-600 mx-4" />
				<!-- <button
					on:click={handleLogout}
					class="text-white text-sm justify-center py-5 max-lg:px-5 gap-2 flex hover:bg-gray-600 w-full"
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
					<span class="hidden lg:block">Logout </span>
				</button> -->
				<SideBarButton text="Logout" isLogout>
					<LogoutIcon />
				</SideBarButton>
			</div>
		</div>
	</div>
</div>
