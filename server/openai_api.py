import openai


def query_openai(messages):
    # TODO: FOR TESTING PURPOSES CROP
	chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=30)
	return chat_completion.choices[0].message.content


def query_with_prompts(system_prompt, user_prompt):
    if system_prompt:
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
    else:
         messages = [{"role": "user", "content": user_prompt}]
    return query_openai(messages)


def write_speech(person_info: str, topic: str, supporting: bool = True):
    speech_type_keyword = "supporting" if supporting else "rebuttal"
    rebuttal_prompt = " Reminder - you are giving a rebuttal speech, so you want to refute the topic." if not supporting else ""
    system_prompt = ""
    user_prompt = f"""You are {person_info}. You are particinpating in a debate competition and are writing a {speech_type_keyword} speech for the following statment: "{topic}". Come up with short speech (120 words or less).{rebuttal_prompt}
Speech:"""
    return query_with_prompts(system_prompt, user_prompt)


def judge_speeches(topic: str, supporting_speech: str, rebuttal_speech: str):
    """
    Uses openai to judge two speeches
    """
    system_prompt = ""
    user_prompt = f"""You are a judge in a debate competition. Given a topic, supporting and rebuttal speeches, grade each speech on a range from 1 to 10 and give a brief summary for why you chose that score.
Topic: {topic}

Supporting speech: {supporting_speech}

Rebuttal speech: {rebuttal_speech}

Supporting speech score, rebuttal speech score, short reasoning for the scores up to 80 words (all comma-separated):
"""
    rv = query_with_prompts(system_prompt, user_prompt)
    print("Judged speeches: " + rv)
    return rv
