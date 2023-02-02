import tkinter
from tkinter import *
from tkinter import ttk

# Import DBHandler class which contains the methods to interact with both MySQL and Mongo database
from boxoffice import DBHandler


def format_movie_detail(movie_detail_dict):
    """This is a static method which takes a dictionary object as parameter and returns in a well formatted structure"""
    movie_info_str = ""
    # Iterate through the items in dictionary
    for key, value in movie_detail_dict.items():
        print(key, '->', movie_detail_dict[key])
        # Add the key to a line
        movie_info_str += key
        # Add a line separator with same length of '-'s as the key string
        movie_info_str += "\n" + "-" * len(key) + "\n"
        # Check if the value is a list.
        if type(value) == list:
            # Iterate through the values and append each value into the return string separated with ','
            for value_item in value:
                movie_info_str += value_item
                movie_info_str += ", "
            # Remove the last ',' from the line
            movie_info_str = movie_info_str[:-2]
        else:
            # Just append the value to the string if value is not a list
            movie_info_str += value
        # Add gap between two key details
        movie_info_str += "\n\n"
    return movie_info_str


class MovieFinder:
    """This class contains the attributes and methods necessary for the UI application.
    The application will enable user to do the following things -
    1. Show dropdown of Genre options for user to select
    2. Retrieve and show the top 50 movies within selected Genre
    4. Show three dropdowns of directors, writers, actors to filter within the list
    5. Show a specific movie detail if user clicks on one of the movies in the list
    """

    def __init__(self):
        """This is the constructor class. It initiates the class variables."""
        # The window surface
        self.surface = None
        # The list of Genres
        self.genres = [
            'Action',
            'Comedy',
            'Family',
            'Horror',
            'Romance',
            'Sport'
        ]
        # Initiate the DBHandler instance. This will in turn initiate the connections to the
        # MySQL and Mongo databases
        self.db_handler = DBHandler()
        # Retrieve the list of directors from MySQL DB
        self.directors = self.db_handler.get_directors()
        # Retrieve the list of writers from MySQL DB
        self.writers = self.db_handler.get_writers()
        # Retrieve the list of actors from MySQL DB
        self.actors = self.db_handler.get_actors()
        # The selected genre Combobox variable
        self.selected_genre = None
        # The selected actor Combobox variable
        self.selected_actor = None
        # The selected writer Combobox variable
        self.selected_writer = None
        # The selected director Combobox variable
        self.selected_director = None

    def show_fields(self):
        """This method renders the initial screen elements for user to input details and submit.
        For this application, this method will show the dropdown of genre options and show a button to show list."""
        # Reset Tk surface
        self.surface = Tk()
        # Set dimension as appropriate for the contained elements and the position of the root surface..
        self.surface.geometry('1200x750+20+10')
        # Assign title for the dialog window
        self.surface.title("Search and view movie details")

        # Create the Combobox for genre options in a LabelFrame
        genre_container = ttk.LabelFrame(self.surface, text="Select genre")
        self.selected_genre = ttk.Combobox(genre_container, width=50, values=sorted(self.genres))
        self.selected_genre.pack()
        genre_container.place(x=50, y=20, height=50, width=500)

        # Create a button to show the top 50 movies for the selected genre.
        # Call "show_movies" method when clicked.
        Button(self.surface, text='Show top 50 movies in genre', command=self.show_movies,
               width=30, bg='light grey', fg='black').place(x=190, y=80)

        # Render the dialog box with all fields
        self.surface.mainloop()

    def show_movies(self):
        """This method reads the selected values for the dropdowns on screen - genre, director, writer, actor.
        It then calls method to retrieve the movies matching the selected criteria.
        It shows the movie names and ranks in the selected genre.
        It creates required method to handle click on any of the movies in the list."""
        # Call 'get_movie_results' method of DBHandler to get the filtered results.
        # The 'show_movies' method will be called for showing the initial 50 results as well,
        # the Combobox variables for selected director, writer, actor will be None that time.
        # So, check for None before attempting to read from the Combobox
        movies_for_genre = self.db_handler.get_movies_results(
            self.selected_genre.get().lower(),
            self.selected_director.get() if self.selected_director is not None else None,
            self.selected_writer.get() if self.selected_writer is not None else None,
            self.selected_actor.get() if self.selected_actor is not None else None)

        # Create a LabelFrame for the results section (including the area for the selected movie detail)
        movie_results = ttk.LabelFrame(self.surface, text="Movies")
        # Place the frame mentioning the position and the dimension
        movie_results.place(x=30, y=120, height=600, width=1140)

        # Create the Combobox for director names in a LabelFrame
        genre_container = ttk.LabelFrame(movie_results, text="Select director")
        self.selected_director = ttk.Combobox(genre_container, width=30, values=sorted(self.directors))
        self.selected_director.pack()
        genre_container.place(x=10, y=10, height=50, width=250)

        # Create the Combobox for writer names in a LabelFrame
        genre_container = ttk.LabelFrame(movie_results, text="Select writer")
        self.selected_writer = ttk.Combobox(genre_container, width=30, values=sorted(self.writers))
        self.selected_writer.pack()
        genre_container.place(x=310, y=10, height=50, width=250)

        # Create the Combobox for actor names in a LabelFrame
        genre_container = ttk.LabelFrame(movie_results, text="Select actor")
        self.selected_actor = ttk.Combobox(genre_container, width=30, values=sorted(self.actors))
        self.selected_actor.pack()
        genre_container.place(x=610, y=10, height=50, width=250)

        # Create a button to show the movies for the selected filter criteria.
        # Call "show_movies" method when clicked.
        Button(movie_results, text='Search in the list', command=self.show_movies,
               width=30, bg='light grey', fg='black').place(x=900, y=25)

        # Create a LabelFrame for the results list.
        movie_results_list = ttk.LabelFrame(movie_results, text="Movie list")
        # Place the frame mentioning the position and the dimension
        movie_results_list.place(x=0, y=70, height=510, width=475)

        # Create a TreeView representation within the LabelFrame area. Use 'Rank' and 'Title' as headings.
        tree = ttk.Treeview(movie_results_list, columns=('Rank', 'Title'), show='headings', height=23)
        # define headings text for rank
        tree.heading('Rank', text="Rank")
        # Place the heading as center aligned
        tree.column('Rank', anchor=CENTER, width=50)
        # define headings text for title
        tree.heading('Title', text="Movie title")
        # Place the heading as center aligned
        tree.column('Title', anchor=CENTER, width=400)

        # Check if there are results returned
        if len(movies_for_genre) > 0:
            # Iterate through the movie list.
            for book_data in movies_for_genre:
                # Insert each record into the tree view by passing the rank and title as a tuple.
                tree.insert('', tkinter.END, values=(book_data[0], book_data[1]))

        # Create a method which will handle the event when one row of the TreeView is clicked.
        def item_selected(event):
            # This method is bound with the <<TreeviewSelect>> event of the Treeview list.
            # This will call 'get_movie_detail' method of the DBHandler class to fetch the details
            # of selected movie.
            for selected_item in tree.selection():
                # Get the selected item
                item = tree.item(selected_item)
                # Get the document from the Mongo db collection matching with the name of the movie
                # Notice that the genre is not passed. Genre is set already with db_handler instance
                # when 'get_movie_results' was called.
                movie_detail = self.db_handler.get_movie_detail(item['values'][1])
                # Remove the auto generated '_id' key from the returned dictionary
                movie_detail.pop("_id")

                # Create a LabelFrame for the movie information
                selected_movie_frame = ttk.LabelFrame(movie_results, text="Movie information")
                # Place the frame mentioning the position and the dimension
                selected_movie_frame.place(x=500, y=70, height=510, width=630)

                # Create a Text element for the movie detail. This is to let user copy from the text.
                text = Text(selected_movie_frame, height=30, width=75)
                # Set a scrollbar for the movie detail frame.
                scroll = Scrollbar(selected_movie_frame)
                text.configure(yscrollcommand=scroll.set)
                # Pack text element to left
                text.pack(side=LEFT)

                # Configure scrollbar for vertical scrolling
                scroll.config(command=text.yview)
                # Pack scrollbar to right of the frame
                scroll.pack(side=RIGHT, fill=Y)

                # Set the value of the Text element with the formatted movie detail.
                text.insert(END, format_movie_detail(movie_detail))

        # Bind the method with TreeViewSelect event.
        tree.bind('<<TreeviewSelect>>', item_selected)

        # Place the TreeView at 0,0 position and stacking from top left.
        tree.grid(row=0, column=0, sticky='NSEW')

        # add a vertical scrollbar to the LabelFrame
        scrollbar_for_list = ttk.Scrollbar(movie_results_list, orient=tkinter.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_for_list.set)
        # Stack the scrollbar on right side
        scrollbar_for_list.grid(row=0, column=1, sticky='NS')


# Check whether the tool is executed from command
if __name__ == '__main__':
    # Create instance of the MovieFinder class and initiate method to display screen components
    movie_finder = MovieFinder()
    movie_finder.show_fields()
