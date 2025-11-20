import sqlite3

def reorder_recipes():
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/recipes.db')
    cursor = conn.cursor()
    
    try:
        # First, check if we need to add the display_order column
        cursor.execute("PRAGMA table_info(recipes)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'display_order' not in columns:
            print("Adding display_order column to recipes table...")
            cursor.execute("ALTER TABLE recipes ADD COLUMN display_order INTEGER DEFAULT 0")
        
        # Get current recipe IDs and names
        cursor.execute("SELECT id, name FROM recipes")
        recipes = cursor.fetchall()
        
        # Create a mapping of recipe names to their current IDs
        recipe_map = {name: id for id, name in recipes}
        
        # Define the desired order (Kare-Kare before Lumpia)
        desired_order = [
            'Adobo',
            'Kare-Kare',
            'Lumpia',
            'Cheese Puto'
        ]
        
        # Update the display_order for each recipe
        for order, name in enumerate(desired_order, start=1):
            if name in recipe_map:
                cursor.execute(
                    "UPDATE recipes SET display_order = ? WHERE name = ?",
                    (order, name)
                )
                print(f"Set {name} to position {order}")
        
        # Verify the order
        cursor.execute("SELECT name, display_order FROM recipes ORDER BY display_order")
        print("\nCurrent recipe order:")
        for name, order in cursor.fetchall():
            print(f"{order}. {name}")
        
        # Commit the transaction
        conn.commit()
        print("\nRecipe order updated successfully!")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    reorder_recipes()
