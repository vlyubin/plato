import sqlite3

def create_tables():
    conn = sqlite3.connect("plato.db")
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS debates (
        debate_id TEXT PRIMARY KEY,
        topic TEXT,
        speaker1 TEXT,
        speaker2 TEXT,
        speech1 TEXT,
        speech2 TEXT,
        judgement TEXT,
        score1 INTEGER,
        score2 INTEGER
    );
    """
    c = conn.cursor()
    c.execute(create_table_sql)
    conn.commit()
    conn.close()


def create_debate(
                debate_id,
                topic,
                speaker1,
                speaker2):
    conn = sqlite3.connect("plato.db")
    sql = f'''INSERT INTO debates(debate_id, topic, speaker1, speaker2)
              VALUES('{debate_id}', '{topic}', '{speaker1}', '{speaker2}')'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


def update_debate(
                debate_id,
                topic=None,
                speaker1=None,
                speaker2=None,
                speech1=None,
                speech2=None,
                judgement=None,
                score1=None,
                score2=None):
    # This is so prone to SQL injections, but I'm too lazy to fix it
    conn = sqlite3.connect("plato.db")
    set_staments = []
    if topic:
        set_staments.append(f"topic = '{topic}'")
    if speaker1:
        set_staments.append(f"speaker1 = '{speaker1}'")
    if speaker2:
        set_staments.append(f"speaker2 = '{speaker2}'")
    if speech1:
        speech1.replace('"', "'")
        set_staments.append(f'speech1 = "{speech1}"')
    if speech2:
        speech2.replace('"', "'")
        set_staments.append(f'speech2 = "{speech2}"')
    if judgement:
        judgement.replace('"', "'")
        set_staments.append(f'judgement = "{judgement}"')
    if score1:
        set_staments.append(f"score1 = '{score1}'")
    if score2:
        set_staments.append(f"score2 = '{score2}'")
    set_stament = ", ".join(set_staments)

    sql = f'''UPDATE debates
              SET {set_stament}
              WHERE debate_id = "{debate_id}"'''
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_all_debates():
    conn = sqlite3.connect("plato.db")
    sql = """
    SELECT * FROM debates;
    """
    c = conn.cursor()
    rows = list(c.execute(sql))
    conn.close()
    return [
        {
            "debate_id": row[0],
            "topic": row[1],
            "speaker1": row[2],
            "speaker2": row[3],
            "speech1": row[4],
            "speech2": row[5],
            "judgement": row[6],
            "score1": row[7],
            "score2": row[8],
        } for row in rows
    ]


def get_debate_by_id(debate_id):
    conn = sqlite3.connect("plato.db")
    sql = f"""
    SELECT * FROM debates WHERE debate_id = "{debate_id}";
    """
    c = conn.cursor()
    rows = list(c.execute(sql))
    conn.close()
    return [
        {
            "debate_id": row[0],
            "topic": row[1],
            "speaker1": row[2],
            "speaker2": row[3],
            "speech1": row[4],
            "speech2": row[5],
            "judgement": row[6],
            "score1": row[7],
            "score2": row[8],        
        } for row in rows
    ]
