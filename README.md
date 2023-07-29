# plato
Debate the best public speakers in the world on any topic you'd like!

## Prerequisites

You will need an Openai API key (we're using gpt3.5) and Elevenlabs API key. If you're new to openai, you'll get ~$7 worth of free usage initially, and any further gpt3.5 usage is pretty cheap. For Elevenlabs, you can get initial monthly membership for $1.

Create `credentials.txt` file in `server` directory that contains the following:

```
OPENAI_KEY=...
ELEVENLABS_KEY=...
```

Then you'll be able to run everything.

## Install dependencies

1. [Optional] Create venv environment using `python3 -m venv .venv`, then activate it `. .venv/bin/activate`
2. Install python dependencies `pip3 install -r requirements.txt`
3. Go to `server/client` and run `npm install`.

## Run software

To run this project, you'll need to run `python3 run.py` in the `server` directory AND `npm run dev` in the `server/client` directory (at the same time).

## Demo video

TODO

## Public hosted version

TODO
