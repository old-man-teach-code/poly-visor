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
					<SideBarButton path="/setting" text="Setting">
						<SettingIcon />
					</SideBarButton>
				</li>
			</ul>
			<div>
				<div class="border-t hidden lg:block border-gray-600 mx-4" />
				<SideBarButton text="Logout" isLogout>
					<LogoutIcon />
				</SideBarButton>
			</div>
		</div>
	</div>
</div>
