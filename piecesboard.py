from enum import Enum
import copy
class HexMoveCaseEvenEven(Enum):
    TOP = (-1, 0)
    DOWN = (1, 0)
    TOP_RIGHT = (-1, 1)
    TOP_LEFT = (-1, -1)
    LOWER_LEFT = (0, -1)
    LOWER_RIGHT = (0, 1)


class HexMoveCaseOddOdd(Enum):
    TOP = (-1, 0)
    DOWN = (1, 0)
    TOP_RIGHT = (0, 1)
    TOP_LEFT = (0, -1)
    LOWER_LEFT = (1, -1)
    LOWER_RIGHT = (1, 1)
class Board:
    def __init__(self, size: int):
        # Initialize a 2D list with zero
        self.board_2d = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        self.pieces = []      # list to store Piece objects
        self.black_piece = [] # list of black pieces
        self.white_piece = [] # list of white pieces

    def check_empty_board(self) -> bool:       
        return all(all(element == 0 for element in row) for row in self.board_2d)
    
    def get_piece_at(self, position):
        x, y = position
        return self.board_2d[x][y]
    
    def place_piece (self, piece : 'Piece' ,position : tuple[int,int] ):
        x, y = position
        self.board_2d[x][y] = piece.type
        piece.position = position
        self.pieces.append(piece)
        if piece.type == -1 or piece.type == -2:
          self.black_piece.append(piece)

        elif piece.type == 1 or piece.type == 2:
          self.white_piece.append(piece)

    

    def make_move(self, move):
        start_pos, end_pos = move
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        type = self.get_piece_at(start_pos)

        if type is None or self.board_2d[end_x][end_y] != 0:
            return self  # Invalid move

        self.board_2d[start_x][start_y] = 0
        self.board_2d[end_x][end_y] = type

        for piece in self.pieces:
            if piece.position == start_pos:
                piece.position = end_pos
                break

        return self
    
    def find_piece_position(self, type):
        """Find the position of a piece by its type on the board."""
        for piece in self.pieces:
            if piece.type == type:
                return piece.position
        return None   
    
    def display(self):
        for row in self.board_2d:
            print(" | ".join(str(cell) if cell else "." for cell in row))
            print("-" * (self.size * 4 - 1))

class Piece:
    def __init__(self, type: int, position: tuple[int, int], insect_type: str, board: Board,player: int=0, color: tuple[int, int, int]=(0, 0, 0), pos_gui: tuple[int, int]=(0, 0),value = 5):
        """
        type
        -1 ---->black
        -2 -----> Queen Bee Black
         1 ----->white
         2 ---->Queen Bee White

        position 
        -1,-1 --> outside the board
        """
        self.type = type
        self.position = position
        self.insect_type = insect_type
        self.valid_moves = None  # or [] depending on the expected usage
        self.board = board
        self.value = value
        self.player = player
        self.color = color
        self.pos_gui = pos_gui
        #self.board.pieces.append(self)


    def check_coordinates(self , x:int, y:int):
    # Check if (x is even and y is even) or (x is odd and y is even)
        if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 == 0):
            return [(x-1,y),(x-1,y+1),(x,y+1),(x+1,y),(x , y-1),(x-1,y-1)]
        else:
            return [(x+1,y),(x+1,y-1),(x+1,y+1),(x,y-1),(x,y+1),(x-1,y)]
            
    def get_free_region_of_piece(self , piece :'Piece') :
        x,y = piece.position
        list =piece.check_coordinates(x,y)
        returnList = []
        for i in range(6) :
          x,y = list[i] 
          if  self.board.board_2d[x][y] == 0:
              returnList.append((x,y))
              
        return returnList
        
    def get_occupied_region_of_piece(self , piece :'Piece') :
        x,y = piece.position
        list =piece.check_coordinates(x,y)
        returnList = []
        for i in range(6) :
          x,y = list[i] 
          if  self.board.board_2d[x][y] != 0:
              returnList.append((x,y))
              
        return returnList
    
    def around_the_hive(self, x: int, y: int) -> list[tuple[int, int]]:
        """
        Determines the intersection of free regions around the hive based on occupied regions.

        Args:
            x (int): The x-coordinate of the piece.
            y (int): The y-coordinate of the piece.

        Returns:
            list[tuple[int, int]]: A list of coordinates representing valid moves around the hive.
        """
        # Get the occupied regions around the given coordinates
        occupied_regions =self.get_occupied_region_of_piece(Piece(self.type, (x, y), self.insect_type, self.board))
        
        # Get the free regions of the given coordinates
        free_regions = set(self.get_free_region_of_piece(Piece(self.type, (x, y), self.insect_type, self.board)))
        
        # Calculate the free regions of all occupied neighbors
        free_around_neighbors = set()
        for neighbor_x, neighbor_y in occupied_regions:
            free_around_neighbors.update(self.get_free_region_of_piece(Piece(self.type, (neighbor_x, neighbor_y), self.insect_type, self.board)))

        # Return the intersection of the free regions
        return list(free_regions & free_around_neighbors)
    
    def check_free_to_slide(self, point1: tuple[int, int], point2: tuple[int, int]) -> bool:
    
        x1, y1 = point1
        x2, y2 = point2

      # Get the surrounding coordinates for both points
        neighbors_point1 = set(self.check_coordinates(x1, y1))
        neighbors_point2 = set(self.check_coordinates(x2, y2))

      # Find the intersection of the neighbors
        intersection = neighbors_point1 & neighbors_point2
        if len(list(intersection))<2:
            return True
        x1, y1 = list(intersection)[0]
        x2, y2 = list(intersection)[1]
      
      # Check if both points on the board are occupied
        if self.board.board_2d[x1][y1] != 0 and self.board.board_2d[x2][y2] != 0:
            return False
        else:
            return True

    def hopper_get_valid_pos_of_direction(self, direction :tuple[int,int], piece_position:tuple[int,int]):
        x,y = piece_position
        if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 == 0):
            if direction == HexMoveCaseEvenEven.TOP.value :
                x,y = piece_position
                while (self.board.board_2d[x][y] !=0):
                    x = x-1

                return (x,y)

            elif direction == HexMoveCaseEvenEven.DOWN.value :
                x,y = piece_position
                while (self.board.board_2d[x][y] !=0):
                    x = x+1

                return (x,y)

            elif direction == HexMoveCaseEvenEven.TOP_LEFT.value :
                counter = 0
                x,y = piece_position 
          
                while(self.board.board_2d[x][y] !=0):
                    y = y-1
                    if counter %2 == 0 :
                        x =x-1
                    counter = counter + 1

                return (x,y)

            elif direction == HexMoveCaseEvenEven.TOP_RIGHT.value:
                counter = 0
                x,y = piece_position 
        
                while(self.board.board_2d[x][y] !=0):
                    y = y+1
                    if counter %2 == 0 :
                        x =x-1
                    counter = counter + 1

                return (x,y)     

            elif direction == HexMoveCaseEvenEven.LOWER_LEFT.value :
                counter = 0
                x,y = piece_position 
                
                while(self.board.board_2d[x][y] !=0):
                    y = y-1
                    if counter %2 != 0 :
                        x =x+1
                    counter = counter + 1

                return (x,y)    

                               

            elif direction == HexMoveCaseEvenEven.LOWER_RIGHT.value :
                counter = 0
                x,y = piece_position 
              
                while(self.board.board_2d[x][y] !=0):
                    y = y+1
                    if counter %2 != 0 :
                        x =x+1
                    counter = counter + 1

                return (x,y)    

                    

                   

        else:
            if direction == HexMoveCaseOddOdd.TOP.value :
                x,y = piece_position
                while (self.board.board_2d[x][y] !=0):
                    x = x-1

                return (x,y)

            elif direction == HexMoveCaseOddOdd.DOWN.value :
                x,y = piece_position
                while (self.board.board_2d[x][y] !=0):
                    x = x+1

                return (x,y)

            elif direction == HexMoveCaseOddOdd.TOP_LEFT.value :
                counter = 0
                x,y = piece_position 
                
                while(self.board.board_2d[x][y] !=0):
                    y = y-1
                    if counter %2 != 0 :
                        x =x-1
                    counter = counter + 1

                return (x,y)         

            elif direction == HexMoveCaseOddOdd.TOP_RIGHT.value:
                counter = 0
                x,y = piece_position 
                
                while(self.board.board_2d[x][y] !=0):
                    y = y+1
                    if counter %2 != 0 :
                        x =x-1
                    counter = counter + 1

                return (x,y)    

                    

                

            elif direction == HexMoveCaseOddOdd.LOWER_LEFT.value :
                counter = 0
                x,y = piece_position 
           

                
                while(self.board.board_2d[x][y] !=0):
                    y = y-1
                    if counter %2 == 0 :
                        x =x+1
                    counter = counter + 1

                return (x,y)                   

            elif direction == HexMoveCaseOddOdd.LOWER_RIGHT.value :
                counter = 0
                x,y = piece_position 
   
             
                while(self.board.board_2d[x][y] !=0):
                    y = y+1
                    if counter %2 == 0 :
                        x =x+1
                    counter = counter + 1

                return (x,y)  


    def is_hive_connected(self):
        visited = set()
        all_pieces = [(i, j) for i in range(self.board.size) for j in range(self.board.size) if self.board.board_2d[i][j] != 0]

        if not all_pieces:
            return True  # Hive is trivially connected if no pieces

        def dfs(position):
            visited.add(position)
            for nx, ny in self.check_coordinates(*position):
                if (nx, ny) in all_pieces and (nx, ny) not in visited:
                    dfs((nx, ny))

        # Start DFS from the first piece
        dfs(all_pieces[0])
        return len(visited) == len(all_pieces)

        

    def check_hive_connectivity_after_move(self, move):
        """
        Check if the hive remains connected after moving the piece to the specified position.

        Args:
            move (tuple[int, int]): The position to move the piece to.

        Returns:
            bool: True if the hive remains connected, False otherwise.
        """
        original_position = self.position
        x, y = original_position
        original_value = self.board.board_2d[move[0]][move[1]]


        # Simulate the move
        self.board.board_2d[x][y] = 0  # Remove from current position
        self.board.board_2d[move[0]][move[1]] = self.type  # Place at new position
        self.position = move  # Update piece's position

        # Check hive connectivity
        hive_connected = self.is_hive_connected()

        # Revert the move
        self.board.board_2d[move[0]][move[1]] = original_value  # Remove from new position
        self.board.board_2d[x][y] = self.type  # Restore to original position
        self.position = original_position  # Restore piece's position

        return hive_connected
    

    def ant_valid_moves(self) -> set[tuple[int, int]]:
      
      x,y = self.position

      # Initialize the set of valid moves
      valid_moves = set()

      # Get the initial positions around the hive
      initial_moves = self.around_the_hive(x, y)

      # Filter initial moves based on sliding rules
      for move in initial_moves:
          if self.check_free_to_slide((x, y), move):
              valid_moves.add(move)

      # Track the size of the set
      previous_size = -1
      self.board.board_2d[x][y]=0
      # Continue expanding valid moves until no new moves are found
      while len(valid_moves) != previous_size:
          previous_size = len(valid_moves)

          # Create a copy of current valid moves to iterate over
          current_moves = list(valid_moves)

          # Check further moves for each current move
          for move_x, move_y in current_moves:
              additional_moves = self.around_the_hive(move_x, move_y)
              for new_move in additional_moves:
                  if self.check_free_to_slide((move_x, move_y), new_move):
                      valid_moves.add(new_move)
      self.board.board_2d[x][y]=self.type
      
      for temp in valid_moves:
          if temp == self.position:
              valid_moves.remove(temp)
              break
      return list(valid_moves)    
        

    def spider_valid_moves(self):
      
      x,y = self.position
      depth = 3

      # Initialize the set for the current level
      current_level_moves = set()

      # Start with the positions around the hive
      initial_moves = self.around_the_hive(x, y)

      # Filter initial moves based on sliding rules
      for move in initial_moves:
          if self.check_free_to_slide((x, y), move):
              current_level_moves.add(move)

      self.board.board_2d[x][y]=0
      # Track moves specifically at the third level
      level_three_moves = set()
      level_two_moves = set()
    # Expand moves for each current valid move
      for move_x, move_y in list(current_level_moves):
          additional_moves = self.around_the_hive(move_x, move_y)
          for new_move in additional_moves:
              if self.check_free_to_slide((move_x, move_y), new_move):
                  level_two_moves.add(new_move)
      for temp in level_two_moves:
          if temp == self.position:
              level_two_moves.remove(temp)
              break
      level_two_moves = level_two_moves.difference(current_level_moves)            
      for move_x, move_y in list(level_two_moves):
          additional_moves = self.around_the_hive(move_x, move_y)
          for new_move in additional_moves:
              if self.check_free_to_slide((move_x, move_y), new_move):
                  level_three_moves.add(new_move)
        
      level_three_moves = level_three_moves.difference(current_level_moves)


      self.board.board_2d[x][y]=self.type
      return list(level_three_moves)

    def get_valid_moves_of_Queen_Bee(self):
        """
        Get valid moves for the Queen Bee that maintain hive connectivity.

        Returns:
            list[tuple[int, int]]: List of valid moves for the Queen Bee.
        """
        free_region = self.get_free_region_of_piece(self)
        valid_moves = []     

        for move in free_region:
            if self.check_hive_connectivity_after_move(move):
                valid_moves.append(move)       

        return valid_moves 
    

    def hopper_valid_moves(self):
        
        list = self.get_occupied_region_of_piece(self) 
        list_valid = []
        x1,y1 =self.position
        for i in range (len(list)):
            x2,y2 = list[i]
            x2 = x2-x1
            y2 = y2-y1
            list_valid.append(self.hopper_get_valid_pos_of_direction((x2,y2),self.position))
        

        if(list_valid):
            #The call of One Hive Rule
            if(self.check_hive_connectivity_after_move(list_valid[0])):
                return list_valid
            else:
                return []
    
    def beetle_valid_moves(self):
        x,y = self.position
        list_final_valid = []
        list_valid = self.check_coordinates(x,y)
        #The call of One Hive Rule
        for i in range(len(list_valid)):
            if(self.check_hive_connectivity_after_move(list_valid[i])):
               list_final_valid.append(list_valid[i])

        return list_final_valid
    
    def get_valid_moves_of_block(self , myTurn : list['Piece'],opponent : list['Piece']) :
        available_list =[]
        excluded_list = []
        for i in range(len(myTurn)):
            available_list.extend(self.get_free_region_of_piece(myTurn[i]))
        available_list = set(available_list)
        
        for i in range(len(opponent)):
          excluded_list.extend(self.get_free_region_of_piece(opponent[i]))
        excluded_list =  set(excluded_list)
        
        

        return  list(available_list - excluded_list)
        
        
        

    def valid_moves_func(self) :
        """
        Determines the valid moves for the piece based on its position and board state.

        Returns:
            list[tuple[int, int]]: A list of valid moves as tuples of (row, column).
        """
        if self.position == (-1, -1):  # The piece is outside the board (not used yet)
            if self.board.check_empty_board():  # If the board is empty
                self.valid_moves = [(4,3)]
                return  self.valid_moves # Place the piece at the center of the board
            elif len(self.board.pieces) == 1:
                old_piece = self.board.pieces[0].position
                x, y = old_piece  # Unpack the tuple
                self.valid_moves = self.check_coordinates(x,y)
                return self.valid_moves
            else :
               if self.type == -1 or self.type == -2:
                   self.valid_moves = self.get_valid_moves_of_block(self.board.black_piece,self.board.white_piece)
                   return self.valid_moves
               elif self.type == 1 or self.type == 2 :
                  self.valid_moves = self.get_valid_moves_of_block(self.board.white_piece,self.board.black_piece)
                  return self.valid_moves
                
        else:
            if self.insect_type == "Hopper":
                return self.hopper_valid_moves()           
            elif self.insect_type == "Beetle":
                return self.beetle_valid_moves()    
            elif self.insect_type == "Qbee":
                return self.get_valid_moves_of_Queen_Bee()
            elif self.insect_type == "Spider":
                return self.spider_valid_moves()
            elif self.insect_type == "Ant":
                return self.ant_valid_moves()
            else:
                return[]

# def main():
#
#      # Create a board with size 3x3
#     board = Board(10)
# #     # board.board_2d[5][5] = -1
# #     # board.board_2d[6][5] = -1
# #     # board.board_2d[6][3] =  1
# #     # board.board_2d[7][4] =  1
#
#
#
#     piece1 =Piece(-1,(-1,-1),"hopper",board)
#     piece2 =Piece(1,(-1,-1),"hopper",board)
#     piece3 =Piece(1,(-1,-1),"hopper",board)
#     piece4 =Piece(1,(-1,-1),"hopper",board)
#     piece5 =Piece(1,(-1,-1),"hopper",board)
#     piece6 =Piece(1,(-1,-1),"hopper",board)
#     piece7 =Piece(1,(-1,-1),"hopper",board)
#     piece8 =Piece(1,(-1,-1),"hopper",board)
#     piece9 =Piece(1,(-1,-1),"hopper",board)
#     piece10 =Piece(1,(-1,-1),"hopper",board)
#     piece11 =Piece(1,(-1,-1),"hopper",board)
#
#
#
#
#
#
#
#
#     board.place_piece(piece1,(4,3))
#
#     board.place_piece(piece2,(3,4))
#     board.place_piece(piece3,(4,4))
#     board.place_piece(piece4,(3,3))
#    #  board.place_piece(piece5,(5,2))
#    #  board.place_piece(piece6,(5,3))
#    #  board.place_piece(piece7,(6,2))
#
#
#     print(piece1.valid_moves_func())


