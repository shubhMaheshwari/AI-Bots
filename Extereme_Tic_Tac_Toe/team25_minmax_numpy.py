from __future__ import print_function

import sys
import random
import signal
import time
import copy
	
import numpy as np


DEPTH = 3

class Team25_minimax_numpy():
	# ply is the character x or o
	def __init__(self,ply):
		self.ply = 1 if ply == 'x' else -1
		self.board = ''
		self.new_board = np.zeros((4,4,4,4))
		self.new_block = np.zeros((4,4))

	def blockshaped(self,arr, nrows, ncols):
		"""
		Return an array of shape (n, nrows, ncols) where
		n * nrows * ncols = arr.size

		If arr is a 2D array, the returned array should look like n subblocks with
		each subblock preserving the "physical" layout of arr.
		"""
		h, w = arr.shape
		return (arr.reshape(h//nrows, nrows, -1, ncols)
					.swapaxes(1,2)
					.reshape(-1, nrows, ncols))	

	def copy_board(self,board):
		string_board = np.array(board.board_status)
		new_board = np.zeros(string_board.shape)
		new_board[string_board == 'x'] = 1
		new_board[string_board == 'o'] = -1
		# reshape to 16 blocks for 16 size
		self.new_board = self.blockshaped(new_board,4,4)
		# reshape again to 4*4 blocks of 16 size
		self.new_board = np.reshape(self.new_board,(4,4,4,4))

		string_block = np.array(board.block_status)
		new_block = np.zeros(string_block.shape)
		new_block[string_block == 'x'] = 1
		new_block[string_block == 'o'] = -1
		new_block[string_block == 'd'] = 2

		self.new_block = new_block 


	def move(self, board, old_move, flag):

		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		
		self.copy_board(board)
		# self.board = copy.deepcopy(board)
		# if(old_move != (-1,-1)):
		# 	self.new_board[old_move[0]/4][old_move[1]/4][old_move[0]%4][old_move[1]%4] == -1*self.ply

		# print("Allowed moves:",possible_moves)
		# print("Calcuated moves",self.find_valid_move_cells(old_move))

		# print("Current Board state")
		# self.board.print_board()

		sub_move,move_value = self.min_max(old_move,self.ply,DEPTH)
		# print("move:", sub_move,"value:",move_value)
		# being send as a numpy int hence error
		# self.new_board[sub_move[0]/4][sub_move[1]/4][sub_move[0]%4][sub_move[1]%4] == self.ply
		# print(old_move,sub_move)
		print("move:",sub_move,"value:",move_value)
		return sub_move
	


	def find_valid_move_cells(self,old_move):
		
		allowed_cells = []
		allowed_block = [old_move[0]%4, old_move[1]%4]
		#checks if the move is a free move or not based on the rules
		if old_move != (-1,-1) and self.new_block[allowed_block[0]][allowed_block[1]] == 0:
			for i in range(4):
				for j in range(4):
					if self.new_board[allowed_block[1]][allowed_block[1]][i][j] == 0:
						allowed_cells.append((i,j))
		else:
			for k in range(4):
				for l in range(4):
					if self.new_block[k][l] == 0:
						for i in range(4):
							for j in range(4):
								if self.new_board[k][l][i][j] == 0:
									allowed_cells.append((i,j))

		print(self.new_board)
		return allowed_cells				



		# #returns the valid cells allowed given the last move and the current board state
		# allowed_block = [old_move[0]%4, old_move[1]%4]
		# #checks if the move is a free move or not based on the rules
		# old_move = tuple(old_move)
		# if old_move != (-1,-1) and self.new_block[allowed_block[0]][allowed_block[1]] == 0.0:
		# 	possible_moves = np.dstack(np.where(self.new_board[allowed_block[0]][allowed_block[1]] == 0))[0]
		# 	possible_moves = possible_moves + [4*allowed_block[0],4*allowed_block[1]]

		# else:
		# 	# First find the possible blocks to place
		# 	possible_moves = np.empty((0,2),int)
		# 	avaible_blocks = np.dstack(np.where(self.new_block == 0))[0]
		# 	for x in avaible_blocks:
		# 		possible_moves = np.append(possible_moves,np.dstack(np.where(self.new_board[x[0]][x[1]] == 0))[0] + [4*x[0], 4*x[1]],axis=0)

		# return possible_moves	


	# returns 1 if x won, 0 if continue state ,-1 for o and 2 for draw 
	def find_terminal_state(self,bs):
		#checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher blocks in case of a draw
		bs_t = bs.T
		for i in range(4):
			row = bs[i]							#i'th row 
			
			#print row,col
			#checking if i'th row or i'th column has been won or not
			if (row[0] ==1 or row[0] == -1) and (np.count_nonzero(row == row[0]) == 4):	
				return row[0]

			col = bs_t[i]			#i'th column	
			if (col[0] ==1 or col[0] == -1) and (np.count_nonzero(col == col[0]) == 4):
				return col[0]


		#checking if diamond has been won
		if(bs[1][0] == bs[0][1] == bs[2][1] == bs[1][2]) and (bs[1][0] == 1 or bs[1][0] == -1):
			return bs[1][0]
		if(bs[1][1] == bs[0][2] == bs[2][2] == bs[1][3]) and (bs[1][1] == 1 or bs[1][1] == -1):
			return bs[1][1]
		if(bs[2][0] == bs[1][1] == bs[3][1] == bs[2][2]) and (bs[2][0] == 1 or bs[2][0] == -1):
			return bs[2][0]
		if(bs[2][1] == bs[1][2] == bs[3][2] == bs[2][3]) and (bs[2][1] == 1 or bs[2][1] == -1):
			return bs[2][1]

		left_blocks = np.count_nonzero(bs)	
		if left_blocks < 16:		#if all blocks have not yet been won, continue
			return 0

		elif left_blocks == 16:							#if game is drawn
			return 2

	def check_block_status(self,x,y):
		return self.find_terminal_state(self.new_board[x][y])


	def min_max(self, old_move,ply,depth,alpha = -10000,beta = 10000):		

		bs = self.board 		
		if(depth == 0):
			return old_move, 0

		# print("old move:",old_move)
		possible_moves = self.find_valid_move_cells(old_move)
		if len(possible_moves) == 0 :
			possible_moves = self.find_valid_move_cells((-1,-1))

		if len(possible_moves) == 0:
			winner = self.find_terminal_state(self.new_block)
			# print("winner:",winner,"message:",message)
			if winner == 1 or winner == -1:
				return old_move,winner*5*(DEPTH-depth)
			else: 
				return old_move, 0
		print("possible:",possible_moves)
		
		sub_move = ''
		sub_value = ''
		block_won = 0

		if ply == 1:	
			best_move = (-1,-1) 
			best_val = -10000
			for move in possible_moves:
				self.new_board[move[0]/4][move[0]/4][move[0]%4][move[1]%4] = 1

				winner = self.find_terminal_state(self.new_block)
				# print("winner:",winner)
				if winner == 1:
					return move,5*(DEPTH-depth)

				elif winner == 2:
					return move, 0

				block_won = self.check_block_status(old_move[0]/4,old_move[1]/4)
				# print("block_won:",block_won)
				# self.print_board()


				if block_won == 1:
					# print(block_won,)
					
					self.new_block[move[0]/4][move[1]/4] = 1
					sub_move,sub_value = self.min_max(move,ply,depth -1,alpha,beta)					
					self.new_block[move[0]/4][move[1]/4] = 0
					# Add the reward of winning a block 
					sub_value += DEPTH - depth

				elif block_won == 2:
					self.new_block[move[0]/4][move[1]/4] = 2
					sub_move,sub_value = self.min_max(move,-1*ply,depth -1,alpha,beta)					
					self.new_block[move[0]/4][move[1]/4] = 0
				
				else:
					sub_move,sub_value = self.min_max(move,-1*ply,depth -1,alpha,beta)

				# print("sub_move:",sub_move,"sub_value:",sub_value)
				
				# Alpha beta pruning 
				if sub_value > best_val:
					best_val = sub_value
					best_move = move

				alpha = max(alpha,best_val)

				# print("alpha:",alpha,"beta",beta)
				if(beta <= alpha):
					break	

				self.new_board[move[0]/4][move[0]/4][move[0]%4][move[1]%4] = 0


			return best_move,best_val

		else:
			best_move = (-1,-1)
			best_val  = 10000
			for move in possible_moves:
				self.new_board[move[0]/4][move[0]/4][move[0]%4][move[1]%4] = -1

				# self.print_board()
				winner  = self.find_terminal_state(self.new_block)
				if winner == -1:
					return move,-5*(DEPTH-depth)
				elif winner == 2:
					return move,0 
				# print("winner:",winner,"message:",message)

				block_won = self.check_block_status(old_move[0]/4,old_move[1]/4)
				# print("block_won:",block_won)	
				if block_won == -1:
					self.new_block[move[0]/4][move[1]/4] = -1
					sub_move,sub_value = self.min_max(move,ply,depth -1,alpha,beta)					
					self.new_block[move[0]/4][move[1]/4] = 0
					# Add the reward of winning a block 
					sub_value += depth - DEPTH

				elif block_won == 2:
					self.new_block[move[0]/4][move[1]/4] = 2
					sub_move,sub_value = self.min_max(move,-1*ply,depth -1,alpha,beta)					
					self.new_block[move[0]/4][move[1]/4] = 0
				
				else:
					sub_move,sub_value = self.min_max(move,-1*ply,depth -1,alpha,beta)
				# print("sub_move:",sub_move,"sub_value:",sub_value)

				# Alpha beta pruning 
				if sub_value < best_val:
					best_val = sub_value
					best_move = move

				beta = min(beta,best_val)

				# print("alpha:",alpha,"beta",beta)
				if(beta <= alpha):
					break	

				self.new_board[move[0]/4][move[0]/4][move[0]%4][move[1]%4] = 0
		 		
			return best_move,best_val			
