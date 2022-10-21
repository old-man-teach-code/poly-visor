<div class="w-full px-10">
    <h1 class=" py-5 text-2xl font-semibold">Overview</h1>
        <div class="grid text-center justify-items-center gap-10 grid-cols-4 grid-rows-4 pt-5">
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">CPU Usage</h1></div>
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">Ram Usage</h1></div>
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">Running process</h1></div>
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">Total process</h1></div>
            <div class="border-2 bg-white w-full h-full rounded-xl row-span-3 col-span-4">chart</div>
        </div>
</div>

<!-- <script>
	import { state, allProcessInfo } from '../store/supstore';
</script>

<h1>Welcome to SvelteKit</h1>
{#each Object.entries($state) as [code, name]}
	<h1>{code}</h1>
	<p>{name}</p>
{/each}
{#each $allProcessInfo as api}
	<h1>{api.name}</h1>
	<p>{api.description}</p>
{/each}
{console.log($allProcessInfo)}
    
{#each $allProcessInfo as info }
    <h1>Name: {info.name}</h1>
    <p>Description: {info.description}</p>
    <p>Exit Status: {info.exitstatus}</p>
    <p>Group: {info.group}</p>
    <p>Log file: {info.logfile}</p>
    <p>Now: {info.now}</p>
    <p>Pid: {info.pid}</p>
    <p>Spawnerr: {info.spawnerr}</p>
    <p>Start: {info.start}</p>  
    <p>State: {info.state}</p>
    <p>Statename: {info.statename}</p>
    <p>Error log file: {info.stderr_logfile}</p>
    <p>Out log file: {info.stdout_logfile}</p>
    <p>Stop: {info.stop}</p>
{/each} -->
