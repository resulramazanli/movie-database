# movie_db.py

import json
import os
from datetime import datetime

class MovieDatabase:
    def __init__(self, filename="movies.json"):
        self.filename = filename
        self.movies = self.load_database()
    
    def load_database(self):
        """Load movies from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_database(self):
        """Save movies to JSON file."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, indent=2, ensure_ascii=False)
    
    def add_movie(self, title, year, rating, genre, review=""):
        """Add a new movie to database."""
        # Validation
        if not title or not title.strip():
            return False, "Title cannot be empty"
        
        if not (1900 <= int(year) <= datetime.now().year):
            return False, f"Year must be between 1900 and {datetime.now().year}"
        
        if not (0 <= float(rating) <= 10):
            return False, "Rating must be between 0 and 10"
        
        movie = {
            "id": len(self.movies) + 1,
            "title": title.strip(),
            "year": int(year),
            "rating": float(rating),
            "genre": genre.strip(),
            "review": review.strip(),
            "date_added": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.movies.append(movie)
        self.save_database()
        return True, f"✅ '{title}' added successfully!"
    
    def view_all(self):
        """Display all movies."""
        if not self.movies:
            return "No movies in database."
        
        output = "\n" + "="*80 + "\n"
        output += f"{'ID':<5} {'Title':<30} {'Year':<6} {'Rating':<8} {'Genre':<15}\n"
        output += "="*80 + "\n"
        
        for movie in self.movies:
            output += f"{movie['id']:<5} {movie['title']:<30} {movie['year']:<6} {movie['rating']:<8} {movie['genre']:<15}\n"
        
        return output
    
    def search_by_title(self, search_term):
        """Search movies by title."""
        results = [m for m in self.movies if search_term.lower() in m['title'].lower()]
        return results
    
    def filter_by_genre(self, genre):
        """Filter movies by genre."""
        results = [m for m in self.movies if m['genre'].lower() == genre.lower()]
        return results
    
    def filter_by_rating(self, min_rating, max_rating=10):
        """Filter movies by rating range."""
        results = [m for m in self.movies if min_rating <= m['rating'] <= max_rating]
        return results
    
    def filter_by_year(self, year):
        """Filter movies by year."""
        results = [m for m in self.movies if m['year'] == int(year)]
        return results
    
    def sort_by(self, key, reverse=False):
        """Sort movies by title, rating, or year."""
        valid_keys = ['title', 'rating', 'year']
        if key not in valid_keys:
            return None
        
        return sorted(self.movies, key=lambda x: x[key], reverse=reverse)
    
    def delete_movie(self, movie_id):
        """Delete a movie by ID."""
        for i, movie in enumerate(self.movies):
            if movie['id'] == int(movie_id):
                title = movie['title']
                self.movies.pop(i)
                self.save_database()
                return True, f"✅ '{title}' deleted."
        
        return False, "Movie not found."
    
    def update_movie(self, movie_id, **kwargs):
        """Update movie details."""
        for movie in self.movies:
            if movie['id'] == int(movie_id):
                for key, value in kwargs.items():
                    if key in movie and value:
                        movie[key] = value
                self.save_database()
                return True, f"✅ Movie updated."
        
        return False, "Movie not found."
    
    def get_statistics(self):
        """Get database statistics."""
        if not self.movies:
            return "No movies in database."
        
        ratings = [m['rating'] for m in self.movies]
        genres = set(m['genre'] for m in self.movies)
        years = set(m['year'] for m in self.movies)
        
        avg_rating = sum(ratings) / len(ratings)
        highest_rated = max(self.movies, key=lambda x: x['rating'])
        lowest_rated = min(self.movies, key=lambda x: x['rating'])
        
        stats = f"""
📊 DATABASE STATISTICS
{'='*40}
Total movies: {len(self.movies)}
Average rating: {avg_rating:.1f}/10
Highest rated: {highest_rated['title']} ({highest_rated['rating']}/10)
Lowest rated: {lowest_rated['title']} ({lowest_rated['rating']}/10)
Unique genres: {len(genres)}
Years span: {min(years)} - {max(years)}
"""
        return stats
    
    def export_to_csv(self, filename="movies_export.csv"):
        """Export movies to CSV file."""
        if not self.movies:
            return False, "No movies to export."
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("ID,Title,Year,Rating,Genre,Review,Date Added\n")
                for movie in self.movies:
                    f.write(f"{movie['id']},\"{movie['title']}\",{movie['year']},{movie['rating']},\"{movie['genre']}\",\"{movie['review']}\",{movie['date_added']}\n")
            return True, f"✅ Exported to {filename}"
        except:
            return False, "Export failed."
    
    def display_movie_details(self, movie_id):
        """Display full details of a movie."""
        for movie in self.movies:
            if movie['id'] == int(movie_id):
                details = f"""
{'='*50}
Title: {movie['title']}
Year: {movie['year']}
Rating: {movie['rating']}/10
Genre: {movie['genre']}
Review: {movie['review'] or 'No review yet'}
Date Added: {movie['date_added']}
{'='*50}
"""
                return details
        return "Movie not found."


def display_menu():
    """Display main menu."""
    print("\n" + "="*50)
    print("🎬 MOVIE DATABASE MANAGER")
    print("="*50)
    print("1.  Add movie")
    print("2.  View all movies")
    print("3.  Search by title")
    print("4.  Filter by genre")
    print("5.  Filter by rating")
    print("6.  Sort movies")
    print("7.  View movie details")
    print("8.  Edit movie")
    print("9.  Delete movie")
    print("10. View statistics")
    print("11. Export to CSV")
    print("12. Exit")
    print("="*50)


def display_results(movies):
    """Display search/filter results."""
    if not movies:
        print("No results found.")
        return
    
    print("\n" + "="*80)
    print(f"{'ID':<5} {'Title':<30} {'Year':<6} {'Rating':<8} {'Genre':<15}")
    print("="*80)
    for movie in movies:
        print(f"{movie['id']:<5} {movie['title']:<30} {movie['year']:<6} {movie['rating']:<8} {movie['genre']:<15}")
    print("="*80)


def main():
    db = MovieDatabase()
    
    while True:
        display_menu()
        choice = input("\nEnter choice (1-12): ").strip()
        
        if choice == '1':
            print("\n--- Add New Movie ---")
            title = input("Title: ")
            year = input("Year: ")
            rating = input("Rating (0-10): ")
            genre = input("Genre: ")
            review = input("Review (optional): ")
            
            try:
                success, message = db.add_movie(title, year, rating, genre, review)
                print(message)
            except ValueError:
                print("❌ Invalid input. Please check year and rating.")
        
        elif choice == '2':
            print(db.view_all())
        
        elif choice == '3':
            search = input("\nSearch title: ")
            results = db.search_by_title(search)
            if results:
                display_results(results)
            else:
                print("No results found.")
        
        elif choice == '4':
            genre = input("\nEnter genre: ")
            results = db.filter_by_genre(genre)
            if results:
                display_results(results)
            else:
                print("No movies in that genre.")
        
        elif choice == '5':
            try:
                min_rating = float(input("Minimum rating (0-10): "))
                results = db.filter_by_rating(min_rating)
                if results:
                    display_results(results)
                else:
                    print("No movies match that rating.")
            except ValueError:
                print("❌ Invalid rating.")
        
        elif choice == '6':
            print("\nSort by:")
            print("1. Title")
            print("2. Rating (highest first)")
            print("3. Year (newest first)")
            sort_choice = input("Choice: ")
            
            if sort_choice == '1':
                results = db.sort_by('title')
            elif sort_choice == '2':
                results = db.sort_by('rating', reverse=True)
            elif sort_choice == '3':
                results = db.sort_by('year', reverse=True)
            else:
                print("Invalid choice.")
                continue
            
            display_results(results)
        
        elif choice == '7':
            movie_id = input("\nEnter movie ID: ")
            print(db.display_movie_details(movie_id))
        
        elif choice == '8':
            movie_id = input("\nEnter movie ID to edit: ")
            print("Leave blank to skip a field.")
            title = input("New title: ")
            rating = input("New rating: ")
            review = input("New review: ")
            
            kwargs = {}
            if title:
                kwargs['title'] = title
            if rating:
                kwargs['rating'] = float(rating)
            if review:
                kwargs['review'] = review
            
            if kwargs:
                success, message = db.update_movie(movie_id, **kwargs)
                print(message)
            else:
                print("No changes made.")
        
        elif choice == '9':
            movie_id = input("\nEnter movie ID to delete: ")
            success, message = db.delete_movie(movie_id)
            print(message)
        
        elif choice == '10':
            print(db.get_statistics())
        
        elif choice == '11':
            filename = input("Export filename (default: movies_export.csv): ").strip()
            if not filename:
                filename = "movies_export.csv"
            success, message = db.export_to_csv(filename)
            print(message)
        
        elif choice == '12':
            print("\nThanks for using Movie Database! 🎬")
            break
        
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()