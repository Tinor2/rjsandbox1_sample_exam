import sqlite3

def add_missing_recipes():
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/recipes.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Check if Kare-Kare exists
        cursor.execute("SELECT COUNT(*) FROM recipes WHERE name = 'Kare-Kare'")
        if cursor.fetchone()[0] == 0:
            print("Adding Kare-Kare recipe...")
            cursor.execute("""
                INSERT INTO recipes (
                    name, category, short_description, long_description,
                    ingredients_text, directions_text, image_path, image_alt,
                    prep_time, cook_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'Kare-Kare',
                'Main Course',
                'A rich peanut stew traditionally served with oxtail, vegetables, and bagoong.',
                'Kare-Kare features slow-cooked meat and vegetables in a creamy peanut sauce, often paired with shrimp paste for savoury contrast.',
                '1 kg oxtail or beef shanks\n2 cups water or beef stock\n1/2 cup peanut butter\n1/4 cup toasted ground rice\n1 bunch pechay (bok choy)\n1 medium eggplant, sliced\n1 banana blossom, sliced\n2 tbsp annatto seeds in water\nSalt and pepper to taste',
                '1. Simmer meat in water or stock until tender, skimming excess fat.\n2. Add peanut butter, ground rice, and annatto water; stir until sauce thickens.\n3. Add vegetables and cook until tender.\n4. Season and serve with shrimp paste.',
                'images/about.webp',
                'Bowl of kare-kare stew with vegetables',
                '25 min',
                '1 hr 30 min'
            ))
        
        # Check if Cheese Puto exists
        cursor.execute("SELECT COUNT(*) FROM recipes WHERE name = 'Cheese Puto'")
        if cursor.fetchone()[0] == 0:
            print("Adding Cheese Puto recipe...")
            cursor.execute("""
                INSERT INTO recipes (
                    name, category, short_description, long_description,
                    ingredients_text, directions_text, image_path, image_alt,
                    prep_time, cook_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'Cheese Puto',
                'Dessert',
                'Soft and fluffy rice cakes topped with cheese, a popular Filipino snack.',
                'Puto is a traditional Filipino steamed rice cake, often served as a snack or for breakfast. This version is topped with cheese for extra flavor.',
                '2 cups rice flour\n1 cup sugar\n1 tbsp baking powder\n1/4 tsp salt\n1 1/2 cups water\n1/2 cup evaporated milk\n2 eggs\n1/4 cup melted butter\n1/2 cup grated cheddar cheese',
                '1. In a bowl, mix rice flour, sugar, baking powder, and salt.\n2. Add water, milk, eggs, and melted butter. Mix until smooth.\n3. Pour batter into greased muffin tins, filling each about 3/4 full.\n4. Top with grated cheese.\n5. Steam for 20-25 minutes or until a toothpick comes out clean.\n6. Let cool before serving.',
                'images/about.webp',
                'Steamed rice cakes with cheese topping',
                '15 min',
                '25 min'
            ))
        
        # Verify the results
        cursor.execute("SELECT name, category, image_path FROM recipes ORDER BY name")
        recipes = cursor.fetchall()
        
        print("\nCurrent recipes in database:")
        for recipe in recipes:
            print(f"- {recipe['name']} ({recipe['category']}) - Image: {recipe['image_path']}")
        
        # Commit the transaction
        conn.commit()
        print("\nDatabase update completed successfully!")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    add_missing_recipes()
