<script>
import PlayFullDiscussion from '../PlayFullDiscussion.svelte';
import { onMount } from 'svelte';

	let host = 'https://debate.lol'; // window.location.protocol + "//" + window.location.hostname
	let addr_backend  = host + '/backend'
	let dialogues = []


	async function get_all_speeches() 
		{
		const url = addr_backend+'/get_all_speeches';

		const requestOptions = 
			{
			method: 'GET',
			headers: 
				{
				'Content-Type': 'application/json'
				},
			};

		try {
			const response = await fetch(url, requestOptions);
			dialogues = await response.json();
			// """
			// Returns all debates in the database. Format is list of:
			// {
			//         "debate_id": row[0],
			//         "topic": row[1],
			//         "speaker1": row[2],
			//         "speaker2": row[3],
			//         "speech1": row[4],
			//         "speech2": row[5],
			//         "judgement": row[6],
			//         "score1": row[7],
			//         "score2": row[8],        
			// }
			// """

			}
		catch (error) 
			{
			console.error('Error fetching data:', error);
			// waiting_for_server = 0
			}
		}
	// waiting_for_server = 1
	onMount(get_all_speeches);
</script>


<svelte:head>
	<title>Debates by others in community</title>
	<meta name="description" content="About this app" />
</svelte:head>

<div class="text-column">
	{#each dialogues as dialogue}
		<div class="dialogue">
			<PlayFullDiscussion  {...dialogue} src={addr_backend+"/static/speeches/"+dialogue.debate_id+".wav"} preload="none"  />
			<!-- {dialogue.topic}
			{dialogue.debate_id} -->
			
		</div>
	{/each}
</div>
