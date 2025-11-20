import sqlite3

def update_recipe_images():
    # Recipe to image mapping
    recipe_images = {
        'Adobo': 'images/uploads/Adobo_DSCF4391_60983fbd.jpg',
        'Kare-Kare': 'images/uploads/kare-kare_5e5d98d4.jpg',
        'Lumpia': 'images/uploads/lumpia.jpg',
        'Cheese Puto': 'images/uploads/cheese-puto_125161b7.jpg'
    }
    
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/recipes.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Update each recipe's image path
        for recipe_name, image_path in recipe_images.items():
            print(f"Updating {recipe_name} with image: {image_path}")
            cursor.execute(
                "UPDATE recipes SET image_path = ? WHERE name = ?",
                (image_path, recipe_name)
            )
        
        # Verify the updates
        cursor.execute("SELECT name, image_path FROM recipes ORDER BY name")
        recipes = cursor.fetchall()
        
        print("\nUpdated recipe images:")
        for recipe in recipes:
            print(f"- {recipe['name']}: {recipe['image_path']}")
        
        # Commit the transaction
        conn.commit()
        print("\nRecipe images updated successfully!")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    update_recipe_images()
