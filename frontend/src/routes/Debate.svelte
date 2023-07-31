<script>

import AudioPlayer from './AudioPlayer.svelte';


export let tracks;
export let topic ;
export let audioElement ;
// export let option1 ;
// export let option2 ;
console.log(tracks)


function autoplay_track()
	{
	}

</script>




<div class="debates">

<h2>{topic}</h2>
<!-- <h3><span class="point_a">{option1}</span> or <span class="point_b">{option2}</span>?</h3> -->

	<div class="tracks">
	{#each tracks as track, i}
		<AudioPlayer  {...track} preload="auto" on:finished={()=>autoplay_track(i+1)} bind:this={audioElement} />
		<br/>
	{/each}
	</div>
</div>



<style>
	h2,h3
		{
		padding:1em;
		margin:0;
		}
	h2  {
		text-align: center;
		font-size : 3em;
		line-height:1.5;
		/* text-transform:capitalize; */
		font-weight:600;
		}
	/* h3  {
		text-align: center;
		font-size : 4em;
		line-height:1.5;
		padding-bottom:0.6em;
		} */
	/* h3 span	{
		text-transform:capitalize;
		} */
	.point_a
		{
		color: #4d8fbe;
		}
	.point_b
		{
		color: #cb7d53;
		}

	
</style>
