import sqlite3
from pathlib import Path

def clean_recipes():
    # Path to the database
    db_path = Path('instance/recipes.db')
    
    # Connect to the SQLite database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Get the count of recipes before deletion
        cursor.execute("SELECT COUNT(*) FROM recipes")
        before_count = cursor.fetchone()[0]
        print(f"Total recipes before cleanup: {before_count}")
        
        # Delete all recipes except the specified ones
        cursor.execute("""
            DELETE FROM recipes 
            WHERE name NOT IN ('Adobo', 'Kare-Kare', 'Lumpia', 'Cheese Puto')
        """)
        
        # Get the count of recipes after deletion
        cursor.execute("SELECT COUNT(*) FROM recipes")
        after_count = cursor.fetchone()[0]
        print(f"Total recipes after cleanup: {after_count}")
        print(f"Removed {before_count - after_count} recipes.")
        
        # List the remaining recipes
        cursor.execute("SELECT name FROM recipes")
        remaining = [row[0] for row in cursor.fetchall()]
        print("\nRemaining recipes:")
        for recipe in remaining:
            print(f"- {recipe}")
        
        # Commit the transaction
        conn.commit()
        print("\nCleanup completed successfully!")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    clean_recipes()
