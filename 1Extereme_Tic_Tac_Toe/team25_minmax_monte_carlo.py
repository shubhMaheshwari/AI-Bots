import sys
import random
import signal
import time
import copy
	

class Team25_minimax_monte_carlo():
	# ply is the character x or o
	def __init__(self,ply,depth):
		self.block_number = 0
		self.ply = 1 if ply == 'x' else 0
		self.board = ''	
		self.turn = 2
		self.depth = depth
		self.explore = self.turn
		self.time = 0
		self.monte_carlo_time = 0
		self.search_time = 0
		pass

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		# print("Allowed moves:",possible_moves)
		self.board = copy.deepcopy(board)
		# print("Current Board state")
		# self.board.print_board()
		self.time = time.time()
		# IDA instead of DFS

		# for i in range(1,self.turn):
		sub_move,move_value = self.min_max(old_move,self.ply,self.depth)
		print("move:",sub_move,"value:",move_value,"ply:",self.ply)
		

		self.turn += 2

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

				block_won = bs.check_block_status(move[0]/4,move[1]/4,'x')
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


				block_won = bs.check_block_status(move[0]/4,move[1]/4,'o')
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