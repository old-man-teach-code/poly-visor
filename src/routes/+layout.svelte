<script>
	import Sidebar from '../components/SideBar.svelte';
	import '../app.css';
</script>

<!-- Import sidebar -->
<Sidebar />
<div class="sm:pl-56">
	<slot />
</div>

<style>
</style>
