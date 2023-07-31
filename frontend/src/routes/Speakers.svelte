<script>
import { createEventDispatcher } from 'svelte';
const dispatch = createEventDispatcher();

export let side='A';
export let chosen='';
export let speakers=[];



function handleSelection(x)
	{
	chosen=x
	dispatch('message', chosen);
	}


function change_name(speaker)
	{
	dispatch('message', speaker);
	chosen=speaker
	dispatch('message', chosen);
	}

</script>




<div class="speakers">
{#each speakers as speaker, i}

	{#if i>0}
		<div on:click={()=>handleSelection(speaker)} class="{chosen == speaker? 'chosen-class' : ''} {side}">{speaker}</div>
	{:else}
		<input on:click={()=>handleSelection(speaker)} on:keyup={()=>change_name(speaker)} class="{chosen == speaker? 'chosen-class' : ''} {side}" bind:value={speaker}/>
	{/if}
	<!-- <div>{speaker}</div> -->
{/each}
</div>



<style>
	.speakers 
		{
		flex-direction: row
		}
	.speakers > div
	,.speakers > input
		{
		width:100%;
		box-sizing:border-box;
		cursor:pointer;
		flex: 1;
		padding: 0.4em 0.6em;
		margin: 0;
		font-size: 1.3em;
		/* border: 1px solid #555; */
		border: 2px solid #222;
		border-radius: 0.3em;
		}

	input{
		background: #222;
		color: #eee;
		}
	.speakers div:hover
	, .speakers input:hover
		{
		color: #fff;

		}
	.chosen-class
		{
		color: #fff;
		background-color: #25455a;
		border-color: #4d8fbe;
		/* background-color: #5a3725; */
		}

	.chosen-class.B
		{
		color: #fff;
		/* background-color: #25455a; */
		/* border-color: #cb7d53; */
		background-color: #5a3725;
		}

	
</style>
