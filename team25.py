import sys
import random
import signal
import time
import copy
	

class Team25():
	# ply is the character x or o
	def __init__(self):
		self.block_number = 0
		self.ply = 1
		self.board = ''	
		self.turn = 2
		self.depth = 8
		self.explore = self.turn
		self.time = 0
		self.monte_carlo_time = 0
		self.search_time = 0
		self.first_try = False
		pass

	def check_block_status(self,x,y,ply):	
		fl = 0
		bs = self.board.board_status

		#checking if a block has been won or drawn or not after the current move
		for i in range(4):
			#checking for horizontal pattern(i'th row)
			if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == ply):
				return 1
			#checking for vertical pattern(i'th column)
			if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == ply):
				return 1

		#checking for diamond pattern
		#diamond 1
		if (bs[4*x+1][4*y] == bs[4*x][4*y+1] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2]) and (bs[4*x+1][4*y] == ply):
			return 1
		#diamond 2
		if (bs[4*x+1][4*y+1] == bs[4*x][4*y+2] == bs[4*x+2][4*y+2] == bs[4*x+1][4*y+3]) and (bs[4*x+1][4*y+1] == ply):
			return 1
		#diamond 3
		if (bs[4*x+2][4*y] == bs[4*x+1][4*y+1] == bs[4*x+3][4*y+1] == bs[4*x+2][4*y+2]) and (bs[4*x+2][4*y] == ply):
			return 1
		#diamond 4
		if (bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x+3][4*y+2] == bs[4*x+2][4*y+3]) and (bs[4*x+2][4*y+1] == ply):
			return 1

		#checking if a block has any more cells left or has it been drawn
		for i in range(4):
			for j in range(4):
				if bs[4*x+i][4*y+j] =='-':
					return -1
		# If no cell is remaining then return 0
		return 0

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		# print("Allowed moves:",possible_moves)
		
		# Check whether we are X or O

		if self.first_try == False:
			self.first_try = True
			if old_move == (-1,-1):
				self.ply = 1
			else:
				self.ply = 0

		self.board = copy.deepcopy(board)
		# print("Current Board state")
		# self.board.print_board()
		self.time = time.time()
		# IDA instead of DFS

		# for i in range(1,self.turn):
		sub_move,move_value = self.min_max(old_move,self.ply,self.depth)
		print("move:",sub_move,"value:",move_value,"ply:",self.ply)
		
		self.turn += 2
		new_time = time.time()


		if(new_time - self.time < 2):
			self.depth = self.depth + 1

		if(new_time - self.time > 15):
			self.depth = self.depth - 1

		print("Total time:",new_time - self.time,"depth:",self.depth)	

		return sub_move



	def min_max(self, old_move,ply,depth,alpha = -10000,beta = 10000):		

		bs = self.board 		
	
		winner, message = bs.find_terminal_state()
		# print("winner:",winner,"message:",message)
		if message == 'WON':
			return old_move,(1 if ply == 1 else -1) *5*(depth)
		elif message == 'DRAW':
			return old_move, 0	

		# print("old move:",old_move)
		possible_moves = bs.find_valid_move_cells(old_move)
		if possible_moves == [] :
			possible_moves = bs.find_valid_move_cells((-1,-1))
		if possible_moves == []:
			bs.print_board()
			sys.exit()	
		# possible_moves = possible_moves[0:16:4]
		
		# print("possible:",possible_moves)
	
		random.shuffle(possible_moves)


		if(depth == 0):
			return old_move, 0




		sub_move = ''
		sub_value = 0
		block_won = 0


		# print("Starting Loop")
		if ply == 1:	
			best_move = '' 
			best_val = -10000
			for move in possible_moves:
				
				bs.board_status[move[0]][move[1]] = 'x'

				block_won = self.check_block_status(move[0]/4,move[1]/4,'x')
				# print("block_won:",block_won)
				# bs.print_board()

				if block_won == 1:
					bs.block_status[move[0]/4][move[1]/4] = 'x'
					sub_move,sub_value = self.min_max(move,ply,depth -1,alpha,beta)					
					bs.block_status[move[0]/4][move[1]/4] = '-'
					# Add the reward of winning a block 
					sub_value += depth

				elif block_won == 0:
					bs.block_status[move[0]/4][move[1]/4] = 'd'
					sub_move,sub_value = self.min_max(move,ply^1,depth -1,alpha,beta)					
					bs.block_status[move[0]/4][move[1]/4] = '-'
				
				else:
					sub_move,sub_value = self.min_max(move,ply^1,depth -1,alpha,beta)

				# print("sub_move:",sub_move,"sub_value:",sub_value)
				
				# Alpha beta pruning 
				if sub_value > best_val:
					best_val = sub_value
					best_move = move

				alpha = max(alpha,best_val)

				# print("alpha:",alpha,"beta",beta)
				bs.board_status[move[0]][move[1]] = '-'


				if(beta <= alpha):
					break	

				tmove = time.time()

				if(tmove - self.time > 15):
					break

			# print(best_move,best_val) 		

			return best_move,best_val

		else:
			best_move = ''
			best_val  = 10000
			for move in possible_moves:
				
				bs.board_status[move[0]][move[1]] = 'o'


				block_won = self.check_block_status(move[0]/4,move[1]/4,'o')
				# print("block_won:",block_won)	
				if block_won == 1:
					bs.block_status[move[0]/4][move[1]/4] = 'o'
					sub_move,sub_value = self.min_max(move,ply,depth -1,alpha,beta)					
					bs.block_status[move[0]/4][move[1]/4] = '-'
					# Add the reward of winning a block 
					sub_value -= depth

				elif block_won == 0:
					bs.block_status[move[0]/4][move[1]/4] = 'd'
					sub_move,sub_value = self.min_max(move,ply^1,depth -1,alpha,beta)					
					bs.block_status[move[0]/4][move[1]/4] = '-'
				
				else:
					sub_move,sub_value = self.min_max(move,ply^1,depth -1,alpha,beta)
				# print("sub_move:",sub_move,"sub_value:",sub_value)

				# Alpha beta pruning 
				if sub_value < best_val:
					best_val = sub_value
					best_move = move

				beta = min(beta,best_val)

				# print("alpha:",alpha,"beta",beta)
				bs.board_status[move[0]][move[1]] = '-'
				
				if(beta <= alpha):
					break		


				tmove = time.time()

				if(tmove - self.time > 15):
					break

			# except Exception as e:
			# 	print(possible_moves)
			# 	print(e)
			# 	exit()
			# print(best_move,best_val)		

			return best_move,best_val