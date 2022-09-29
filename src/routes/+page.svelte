<script>
    import {supervisor} from "../store/supstore";
    let sups = $supervisor;
</script>
<h1>Welcome to SvelteKit</h1>
{#each Object.entries(sups) as [code, name]}
    <h1>{code}</h1>
    <p>{name}</p>
{/each}
<!-- <h1>{sups}</h1> -->