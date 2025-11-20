import sqlite3
from pathlib import Path

def clean_duplicates():
    # Path to the database
    db_path = Path('instance/recipes.db')
    
    # Connect to the SQLite database
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Get all recipes
        cursor.execute("SELECT * FROM recipes ORDER BY name")
        recipes = cursor.fetchall()
        
        # Dictionary to track unique recipes by name
        unique_recipes = {}
        
        for recipe in recipes:
            name = recipe['name']
            
            # If we haven't seen this recipe name before, or if this version has a more specific image path
            if name not in unique_recipes or ('uploads' in recipe['image_path'] and 'uploads' not in unique_recipes[name]['image_path']):
                unique_recipes[name] = dict(recipe)
        
        # Delete all current recipes
        cursor.execute("DELETE FROM recipes")
        
        # Insert the unique recipes back
        for recipe in unique_recipes.values():
            # Ensure the image path is valid, default to about.webp if not found
            image_path = recipe['image_path']
            
            # Check if the image exists, if not use about.webp
            if not (Path('static') / image_path).exists():
                print(f"Warning: Image not found: {image_path}, using default image")
                image_path = 'images/about.webp'
            
            # Insert the recipe with the corrected image path
            cursor.execute("""
                INSERT INTO recipes (name, category, short_description, long_description, 
                                   ingredients_text, directions_text, image_path, image_alt,
                                   prep_time, cook_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                recipe['name'],
                recipe.get('category', 'Main Course'),
                recipe.get('short_description', ''),
                recipe.get('long_description', ''),
                recipe.get('ingredients_text', ''),
                recipe.get('directions_text', ''),
                image_path,
                recipe.get('image_alt', ''),
                recipe.get('prep_time', ''),
                recipe.get('cook_time', '')
            ))
        
        # Verify the results
        cursor.execute("SELECT id, name, image_path FROM recipes ORDER BY name")
        remaining = cursor.fetchall()
        
        print("\nFinal recipes in database:")
        for recipe in remaining:
            print(f"- {recipe['name']} (Image: {recipe['image_path']})")
        
        # Commit the transaction
        conn.commit()
        print("\nDatabase cleanup completed successfully!")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    clean_duplicates()
