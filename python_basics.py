import csv

## TO DO: Create a class Player
#         Attributes: alias, points

class SomeGame:
    """
        Create a constructor for this class
        Three parameters: self, title, num_players
        'self' is conceptually equivalent to the **this** object

    """
    def __init__(self, title, num_players):
        self.title = title
        self.num_players = num_players
        self.players =  list()


    """
        Define a function that displays a welcome message
        Notice that unlike other languages, you don't have to
        explicitly specify the return type.

    """
    def welcome_message(self):
        return f"Welcome to {self.title}!"


    ## Another function that specifies data types
    def update_title(self, newTitle:str) -> str:
        # Update the title
        self.title = newTitle

        # Return the new title for the sake of the example
        return self.title


    """
        Define a function that creates 'num_players' players
        using the class defined above.
        Function name: add_players
        Arguments: list of dictionaries with player information `player_list`

    """
    # def ...
        # add element to a list: aList.append(object)


## To prevent executing the code if the file is not
#  run as the main file.
if __name__ == "__main__":

    ## ----- Player information dictionaries
    player1 = {
        "alias": "player1",
        "points": 2
    }
    player2 = {
        "alias": "player2",
        "points": 5
    }

    list_of_players = [player1, player2]
    print("There are ", len(list_of_players), " players:")
    print(f"   P1: {player1['alias']} \n   P2: {player2['alias']}")

    ## ----- Declaring variables does not require specifying the type
    title = "Some Game"
    num_players = len(list_of_players)

    ## ----- Initializing an object of type SomeGame
    print("\nStarting the game ...\n")
    game = SomeGame(title, num_players)

    ## ----- Call a method using the object
    ## Display the welcome message
    print(game.welcome_message())

    ## ----- Create player objects
    # game.add_players()

    ## ----- Create a sample CSV file and write player information
    with open("player_data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Alias", "Points"])
        ## This assumes only two players.
        #  Re-write it to use a loop instead that
        #  displays the list of players: list_of_players
        writer.writerow([player1["alias"], player1["points"]])
        writer.writerow([player2["alias"], player2["points"]])

    ## ----- Read the CSV file
    with open("player_data.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print("CSV Row:", row)
