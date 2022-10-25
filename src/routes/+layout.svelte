<script>
    import Sidebar from "../components/sidebar.svelte";
    import "../app.css";
</script>
<div class="flex justify-items-center">
    <Sidebar/>
    <slot/>
</div>

<style>
</style>