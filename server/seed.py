#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Recipe, User

fake = Faker()

with app.app_context():
    # Deleting all records
    print("Deleting all records...")
    Recipe.query.delete()
    User.query.delete()
    db.session.commit()  # Ensure changes are committed after deletion

    # Creating users
    print("Creating users...")

    users = []
    usernames = set()  # Using a set to ensure unique usernames

    for _ in range(20):
        username = fake.first_name()

        # Ensure the username is unique
        while username in usernames:
            username = fake.first_name()
        usernames.add(username)

        user = User(
            username=username,
            bio=fake.paragraph(nb_sentences=3),
            image_url=fake.image_url(),  # Use a more appropriate Faker method for image URLs
        )

        # Hashing the password instead of storing plaintext
        user.password_hash = f"{username}password"

        users.append(user)

    db.session.add_all(users)
    db.session.commit()  # Commit users to generate IDs for relationships

    # Creating recipes
    print("Creating recipes...")

    recipes = []
    for _ in range(100):
        recipe = Recipe(
            title=fake.sentence(nb_words=4),  # Limit sentence length for titles
            instructions=fake.paragraph(nb_sentences=8),
            minutes_to_complete=randint(15, 90),
            user=rc(users),  # Assign a random user to the recipe
        )

        recipes.append(recipe)

    db.session.add_all(recipes)
    db.session.commit()  # Commit all recipes

    print("Seeding complete.")
