import sqlite3, os
DB = os.path.join(os.path.dirname(__file__), "vocab.db")
conn = sqlite3.connect(DB)
c = conn.cursor()

# Insert sample data only if tables are empty to avoid duplicates
def table_has_rows(table):
    c.execute(f"SELECT COUNT(*) FROM {table}")
    return c.fetchone()[0] > 0

if not table_has_rows('vocabulary'):
    c.executemany("""
    INSERT INTO vocabulary (word, meaning, topic) VALUES (?, ?, ?)
    """, [
        ('relentless', 'không ngừng nghỉ', 'Tính cách'),
        ('betrayal', 'sự phản bội', 'Cảm xúc'),
        ('separation', 'sự chia ly', 'Gia đình'),
        ('protagonist', 'nhân vật chính', 'Văn học'),
        ('terrorist', 'kẻ khủng bố', 'Thời sự'),
    ])
    print('Inserted sample vocabulary.')

if not table_has_rows('grammar'):
    c.executemany("""
    INSERT INTO grammar (title, description, example) VALUES (?, ?, ?)
    """, [
        ('Present Simple', 'Thì hiện tại đơn – diễn tả thói quen, chân lý', 'I go to school every day.'),
        ('Past Continuous', 'Quá khứ tiếp diễn – hành động đang xảy ra trong quá khứ', 'I was reading when she called.'),
        ('Future Perfect', 'Tương lai hoàn thành – hành động hoàn thành trước một thời điểm tương lai', 'By 2025 I will have graduated.'),
    ])
    print('Inserted sample grammar.')

if not table_has_rows('sentence_patterns'):
    c.executemany("""
    INSERT INTO sentence_patterns (pattern, usage, example) VALUES (?, ?, ?)
    """, [
        ('It is time + S + V2/ed', 'Dùng để nói đã đến lúc ai đó nên làm gì', 'It is time we left.'),
        ('S + be interested in + V-ing', 'Diễn tả sự quan tâm, thích thú', 'She is interested in learning English.'),
        ('S + used to + V', 'Thói quen trong quá khứ (bây giờ không còn)', 'I used to play football every afternoon.'),
    ])
    print('Inserted sample sentence patterns.')

conn.commit()
conn.close()
print('✅ seed_data: done.')
