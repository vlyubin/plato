from collections import namedtuple

Speaker = namedtuple("Speaker", "name image_url topics")

SPEAKERS = [
    Speaker("Barack Obama", "", ["Universal basic income a good idea", "US foreign policy during Obama's presidency was bad", "Basketball is better than golf"]),
    Speaker("Donald Trump", "", ["US should build a wall at the southern border", "US is the best country in the world", "Golf is better than basketball"]),
    #Speaker("Elon Musk", "", ["Humanity needs a colony on Mars", "Humanity needs to switch to electric cars ASAP", "DogeCoin is a sound investment"]),
    #Speaker("Taylor Swift", "", ["Mmusic industry is not fair to artists", "Heavy metal is better than pop", "Kanye West is a bad person"]),
    #Speaker("Bill Gates", "", ["Windows is the best OS", "Steve Ballmer was a better CEO than Satya Nadella", "Microsoft should acquire ElevenLabs"]),
    Speaker("Emma Watson", "", ["Europe should accept more refugees", "Hermione should have ended up with Harry instead of Ron"]),
    #Speaker("Steve Jobs", "", ["iOS better than Android", "Stanford is better than Berkeley"]),
]
