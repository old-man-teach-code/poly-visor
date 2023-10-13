<script>
	import Sidebar from '../components/SideBar.svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	$: pathname = $page.url.pathname;

	import '../app.css';
	import LoadingScreen from '../components/LoadingScreen.svelte';

	onMount(() => {
		const token = document.cookie.split(';').find((row) => row.startsWith('accessToken'));
		if (!token) {
			goto('/login');
		}
	});
</script>

<!-- Import sidebar -->
{#if pathname == '/login'}
	<slot />
{:else}
	<div class="flex flex-row w-full max-w-screen min-h-fit h-screen">
		<Sidebar />
		<LoadingScreen />
		<slot />
	</div>
{/if}
