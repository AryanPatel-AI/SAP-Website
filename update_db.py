import sqlite3

def update_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE portfolios ADD COLUMN category TEXT")
        cursor.execute("ALTER TABLE portfolios ADD COLUMN hashtags TEXT")
        cursor.execute("ALTER TABLE portfolios ADD COLUMN details TEXT")
        cursor.execute("ALTER TABLE portfolios ADD COLUMN improvement_tips TEXT")
        conn.commit()
        print("Database updated successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error updating database (columns might already exist): {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    update_db()
