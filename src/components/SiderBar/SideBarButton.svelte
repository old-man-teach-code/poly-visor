<script lang="ts">
	import { page } from '$app/stores';
	import { logout } from '../../store/action';
	$: pathname = $page.url.pathname;

	export let text: string;
	export let isLogout: boolean = false;
	export let path: string = '';

	async function handleLogout() {
		const status = (await logout())?.status;
		if (status === 200) {
			localStorage.clear();
			window.location.href = '/login';
		}
	}
</script>

<a
	on:click={isLogout ? handleLogout : null}
	href={path}
	class=" text-white hover:bg-gray-600 flex flex-row gap-4 w-full lg:py-4 lg:px-10 py-2.5 px-4 {pathname ==
	path
		? 'bg-gray-600'
		: 'bg-sidebar'}"
>
	<slot />
	<p class="hidden lg:block">{text}</p>
</a>
