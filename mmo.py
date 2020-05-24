import psycopg2

    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    c = conn.cursor()
    c.execute("create table if not exists in_battle(\
                   user_id BIGINT,\
                   channel_id BIGINT,\
                   player_hp BIGINT check(player_hp >= 0),\
               )")
    c.execute("create table if not exists player(\
                    user_id BIGINT,\
                    experience BIGINT,\
                    bot BIGINT,\
                )")
    c.execute("create table if not exists channel_status(\
                    channel_id BIGINT,\
                    boss_level BIGINT,\
                    boss_hp BIGINT,\
                    monster BIGINT,\
                )")
    c.execute("create table if not exists item(\
                    user_id BIGINT,\
                    item_id BIGINT,\
                    count BIGINT check(count >= 0),\
                )")
    c.execute("create table if not exists ban_member(\
                    channel_id BIGINT,\
                )")
    c.execute("create table if not exists channel_in_transactio(\
                    channel_id BIGINT,\
                )") 
    c.execute("create table if not exists login(\
                    user_id BIGINT,\
                )")
    c.execute("create table if not exists monster_count(\
                    user_id BIGINT,\
                    count BIGINT,\
                )")
    c.execute("create table if not exists training_question(\
                    user_id BIGINT,\
                    training_question BIGINT,\
                )")
    conn.commit()
    c.close()
    conn.close()
