<script>
	import Sidebar from '../components/SideBar.svelte';
	import { page } from '$app/stores';
	import { beforeUpdate, onMount } from 'svelte';
	import { isAuthenticated, startFetching } from '../store/supstore.js';

	$: pathname = $page.url.pathname;

	import '../app.css';
	import LoadingScreen from '../components/LoadingScreen.svelte';

	onMount(() => {
		if ($isAuthenticated == 'false' && pathname != '/login') {
			window.location.href = '/logcasi in';
		}
		if ($isAuthenticated == 'true' && pathname != '/login') {
			startFetching();
		}
	});
</script>

<!-- Import sidebar -->
{#if pathname == '/login'}
	<slot />
{:else}
	<div class="flex flex-row w-full min-h-screen ">
		<Sidebar />
		<LoadingScreen />
		<slot />
	</div>
{/if}
