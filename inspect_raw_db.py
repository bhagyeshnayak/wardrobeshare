import sqlite3
import os

db_path = 'db.sqlite3'

with open('db_dump.txt', 'w', encoding='utf-8') as f:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        f.write("--- PRODUCTS ---\n")
        cursor.execute("SELECT id, title FROM products_product")
        for row in cursor.fetchall():
            title = row[1]
            f.write(f"ID: {row[0]} | Title: {title}\n")
            if "{{" in title:
                f.write(f"!!! CORRUPTION DETECTED IN ID {row[0]} !!!\n")
            
        f.write("\n--- BOOKINGS ---\n")
        cursor.execute("SELECT id, start_date, end_date FROM bookings_booking")
        for row in cursor.fetchall():
            f.write(f"ID: {row[0]} | Start: {row[1]} | End: {row[2]}\n")
            if str(row[2]) and "{{" in str(row[2]):
                 f.write(f"!!! CORRUPTION DETECTED IN BOOKING {row[0]} !!!\n")

    except Exception as e:
        f.write(f"Error: {e}\n")
    finally:
        if conn:
            conn.close()
