movies = ["Inception", "Mr.Bean", "Interstellar", "Kingdom", "Pushpa"]
print("Your favorite movies:", movies)

# Add a new movie
new_movie = input("Add a new movie: ")
movies.append(new_movie)
print("After adding:", movies)

# Replace one movie
index_to_replace = int(input("Enter the index (1-5) of the movie to replace: ")) - 1
if 0 <= index_to_replace < len(movies):
    new_title = input("Enter the new movie title: ")
    movies[index_to_replace] = new_title
    print("After replacement:", movies)
else:
    print("Invalid index. No replacement done.")

# Remove a movie
remove_movie = input("Enter the title of the movie to remove: ")
if remove_movie in movies:
    movies.remove(remove_movie)
    print("After removal:", movies)
else:
    print(f"'{remove_movie}' not found in the list.")