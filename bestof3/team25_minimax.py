import sys
import random
import signal
import time
import copy
	

class Team25_minimax():
	# ply is the character x or o
	def __init__(self):
		self.block_number = 0
		self.ply = 1 
		self.board = ''	
		self.turn = 2
		self.depth = 8
		self.time = 0
		self.small_board_win = False
		self.eval_time = 0
		self.keys = []
		for i in range(256):
			x = []
			for j in range(3):
				x.append(random.randint(0,1000000))
			self.keys.append(x)

		# Store the value of a state
		self.hash_table = {}
		# Store the depth at which the value is stored
		self.hash_depth = {}	

		pass


	def create_hash_state(self):
		bs = self.board.board_status
		hash_value = 0
		k = 0
		for i in range(16):
			for j in range(16):
				if bs[i][j] == 'x':
					k = 2
				elif bs[i][j] == 'o':
					k = 1

				elif bs[i][j] == '-':
					k = 0

				hash_value ^= self.keys[16*i + j][k]

		return hash_value		
			


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

	def check_block_value(self,x,y,ply):	
		total_ply = 0
		total_dash = 0 
		bs = self.board.board_status
		# print("Checking block status")
		#checking if a block has been won or drawn or not after the current move
		
		for i in range(4):
			cnt_ply = 0 

			#checking for horizontal pattern(i'th row)
			for j in range(4):
				if bs[4*x + i][4*y + j] == ply:
					cnt_ply += 1

				elif bs[4*x + i][4*y + j] == '-':
					total_dash += 1	

				else:
					cnt_ply = 0
					break

			if cnt_ply == 4:
				return 16*(1 if ply == 'x' else -1)		 	

			total_ply += cnt_ply	

			cnt_ply = 0 

			for j in range(4):
				if bs[4*x + j][4*y + i] == ply:
					cnt_ply += 1

				elif bs[4*x + j][4*y + i] == '-':
					total_dash += 1	

				else:
					cnt_ply = 0
					break

			if cnt_ply == 4:
				return 16*(1 if ply == 'x' else -1)

			total_ply += cnt_ply	

		# in case of draw send an exception value
		if total_dash == 0: 
			# print("Evaluated draw")
			return 0	

		#checking for diamond pattern
		for i in range(4):
			cnt_ply = self.check_diamond(i+1,x,y,ply)
			if cnt_ply == 16:
				return cnt_ply
			else:
				total_ply += cnt_ply

		# print("total_ply:",total_ply)
		return total_ply*(1 if ply == 'x' else -1)	

	def find_terminal_state(self,ply):
		#checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher blocks in case of a draw
		bs = self.board.block_status

		total_x = 0
		total_y = 0
		total_ply = 0
		total_dash = 0 
		# print("Checking block status")
		#checking if a block has been won or drawn or not after the current move
		
		for i in range(4):
			cnt_x = 0
			cnt_y = 0
			cnt_ply = 0 

			#checking for horizontal pattern(i'th row)
			for j in range(4):
				if bs[i][ j] == 'x':
					cnt_x += 16


				elif bs[i][ j] == 'o':
					cnt_y += 16	
						
				elif bs[i][ j] == '-':
					total_dash += 1	
					cnt_ply += self.check_block_value(i, j,'x' if ply == 1 else 'o')
				else:
					cnt_ply = 0 
					break

			if cnt_x == 4:
				return 16

			elif cnt_y == 4:
				return -16	

			total_x += cnt_x	
			total_y += cnt_y
			total_ply += cnt_ply	


			cnt_x = 0 
			cnt_y = 0 
			cnt_ply = 0 

			for j in range(4):
				if bs[j][i] == 'x':
					cnt_x += 16


				elif bs[j][i] == 'o':
					cnt_y += 16		

				elif bs[j][i] == '-':
					total_dash += 1
					cnt_ply += self.check_block_value(j, i,'x' if ply == 1 else 'o')

				else:
					cnt_ply = 0
					break

			if cnt_x == 4:
				return 16

			elif cnt_y == 4:
				return -16			 	

			total_x += cnt_x	
			total_y += cnt_y
			total_ply += cnt_ply


		# in case of draw send an exception value
		if total_dash == 0: 
			print("Evaluated draw")
			return 0

		#checking for diamond pattern
		for i in range(4):
			cnt_ply = self.block_check_diamond(i+1,'x' if ply == 1 else 'o')
			if cnt_ply == 16*ply:
				return cnt_ply
			else:
				total_ply += cnt_ply

		# print("total_x:",total_x,"total_y:",total_y,"total_ply:",total_ply)	
		return total_x - total_y + total_ply # 4*12 assuming check state returns < 4 


	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		# print("Allowed moves:",possible_moves)
		
		# Check whether we are X or O
		if flag == 'x':
			self.ply = 1
		elif flag == 'o':
			self.ply = -1

		self.board = copy.deepcopy(board)
		hash_value = self.create_hash_state()
		# print("Current Board state")
		# self.board.print_board()

		self.eval_time = 0
		self.time = time.time()
		# IDA instead of DFS

		# for i in range(1,self.turn):
		sub_move,move_value = self.min_max(old_move,self.ply,self.depth, hash_value,ispolicy = 1)
		print("turn:",self.turn,"move:",sub_move,"value:",move_value,"ply:",self.ply)
		self.turn += 2
		new_time = time.time()


		if(new_time - self.time < 2):
			self.depth = self.depth + 1

		if(new_time - self.time > 15):
			self.depth = self.depth - 1

		print("Total time:",new_time - self.time,"depth:",self.depth)	
		print("Eval time:",self.eval_time)
		return sub_move

	def min_max(self, old_move,ply,depth,hash_value,alpha = -10000,beta = 10000,ispolicy=1):		

		bs = self.board 		
		if(depth == 0):
			return old_move, self.find_terminal_state(ply)
			# return old_move,0
		


		winner, message = bs.find_terminal_state()
		# print("winner:",winner,"message:",message)
		if message == 'WON':
			return old_move,  ply*self.depth*48*(depth)
		elif message == 'DRAW':
			return old_move, 0	

		# print("old move:",old_move)
		possible_moves = bs.find_valid_move_cells(old_move)
		if possible_moves == [] :
			possible_moves = bs.find_valid_move_cells((-1,-1))
		if possible_moves == []:
			bs.print_board()
		# possible_moves = possible_moves[0:16:4]
		
		# print("possible:",possible_moves)
		random.shuffle(possible_moves)
		

		sub_move = ''
		sub_value = 0
		block_won = 0

		# print("Current hash_value:",hash_value)
		# print("Starting Loop")
		if ply == 1:	
			best_move = '' 
			best_val = -10000
			for move in possible_moves:
				
				bs.board_status[move[0]][move[1]] = 'x'
				hash_value ^= self.keys[16*move[0] + move[1]][2]

				# print("block_won:",block_won)
				# bs.print_board()

				if hash_value in self.hash_depth and self.hash_depth[hash_value] >= depth:
					sub_value = self.hash_table[hash_value]
					print("Using saved value:",sub_value)

				else:
					block_won = self.check_block_status(move[0]/4,move[1]/4,'x')
					if block_won == 1:
						bs.block_status[move[0]/4][move[1]/4] = 'x'
						sub_move,sub_value = self.min_max(move,ply,depth -1,hash_value,alpha,beta)					
						bs.block_status[move[0]/4][move[1]/4] = '-'
						# Add the reward of winning a block 
						sub_value += 48*depth

					elif block_won == 0:
						bs.block_status[move[0]/4][move[1]/4] = 'd'
						sub_move,sub_value = self.min_max(move,-1*ply,depth -1,hash_value,alpha,beta)					
						bs.block_status[move[0]/4][move[1]/4] = '-'
					
					else:
						sub_move,sub_value = self.min_max(move,-1*ply,depth -1,hash_value,alpha,beta)

				# print("sub_move:",sub_move,"sub_value:",sub_value)
				
				# Alpha beta pruning 
				if sub_value > best_val:
					best_val = sub_value
					best_move = move

				alpha = max(alpha,best_val)

				# print("alpha:",alpha,"beta",beta)
				hash_value ^= self.keys[16*move[0] + move[1]][2]
				bs.board_status[move[0]][move[1]] = '-'


				if(beta <= alpha):
					break	

				tmove = time.time()

				if(tmove - self.time > 15):
					break

			# print(best_move,best_val) 	
			if hash_value in self.hash_depth and self.hash_depth[hash_value] > depth:
				print("Error while hashing the move", self.hash_depth[hash_value],depth)
			
			else:
				self.hash_table[hash_value] = best_val
				self.hash_depth[hash_value] = depth
				# print("Saving hash_value:",hash_value,self.hash_table[hash_value])

			return best_move,best_val

		else:
			best_move = ''
			best_val  = 10000
			for move in possible_moves:
				
				bs.board_status[move[0]][move[1]] = 'o'
				hash_value ^= self.keys[16*move[0] + move[1]][1]

				if hash_value in self.hash_depth and self.hash_depth[hash_value] >= depth:
					sub_value = self.hash_table[hash_value]
					print("Using saved value:",sub_value)

				else:
					block_won = self.check_block_status(move[0]/4,move[1]/4,'o')
					# print("block_won:",block_won)	
					if block_won == 1:
						bs.block_status[move[0]/4][move[1]/4] = 'o'
						sub_move,sub_value = self.min_max(move,ply,depth -1,hash_value,alpha,beta)					
						bs.block_status[move[0]/4][move[1]/4] = '-'
						# Add the reward of winning a block 
						sub_value -= 48*depth

					elif block_won == 0:
						bs.block_status[move[0]/4][move[1]/4] = 'd'
						sub_move,sub_value = self.min_max(move,-1*ply,depth -1,hash_value,alpha,beta)					
						bs.block_status[move[0]/4][move[1]/4] = '-'
					
					else:
						sub_move,sub_value = self.min_max(move,-1*ply,depth -1,hash_value,alpha,beta)

				# print("sub_move:",sub_move,"sub_value:",sub_value)

				# Alpha beta pruning 
				if sub_value < best_val:
					best_val = sub_value
					best_move = move

				beta = min(beta,best_val)

				# print("alpha:",alpha,"beta",beta)
				hash_value ^= self.keys[16*move[0] + move[1]][1]
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
			if hash_value in self.hash_depth and self.hash_depth[hash_value] > depth:
				print("Error while hashing the move", self.hash_depth[hash_value],depth)
				
			else:
				self.hash_table[hash_value] = best_val
				self.hash_depth[hash_value] = depth
				# print("Saving hash_value:",hash_value,self.hash_table[hash_value])

			return best_move,best_val		



	def check_diamond(self,ind,x,y,ply):
		bs = self.board.board_status
		if ind == 1:	
			#checking for diamond pattern
			#diamond 1
			cnt_ply = 0
			cnt_dash = 0

			if bs[4*x+1][4*y] == ply:
				cnt_ply +=1

			elif bs[4*x+1][4*y] == '-':
				cnt_dash +=1
		
			else:
				return 0

			if bs[4*x][4*y +1] == ply:
				cnt_ply +=1

			elif bs[4*x][4*y + 1] == '-':
				cnt_dash +=1	

			else:
				return 0
		

			if bs[4*x+2][4*y +1] == ply:
				cnt_ply +=1

			elif bs[4*x+2][4*y +1]  == '-':
				cnt_dash +=1

			else:
				return 0


			if bs[4*x+1][4*y +2] == ply:
				cnt_ply +=1

			elif bs[4*x+1][4*y +2]  == '-':
				cnt_dash +=1	

			else:
				return 0 

			if cnt_ply == 4:
				return 16*(1 if ply == 'x' else -1)

			return cnt_ply		

		elif ind == 2:	
			#diamond 2
			cnt_ply = 0
			cnt_dash = 0

			if bs[4*x+1][4*y+1] == ply:
				cnt_ply +=1

			elif bs[4*x+1][4*y+1] == '-':
				cnt_dash +=1
			
			else:
				return 0

			if bs[4*x][4*y+2] == ply:
				cnt_ply +=1

			elif bs[4*x][4*y+2] == '-':
				cnt_dash +=1	

			else:
				return 0

			if bs[4*x+2][4*y +2] == ply:
				cnt_ply +=1

			elif bs[4*x+2][4*y +2]  == '-':
				cnt_dash +=1

			else:
				return 0

			if bs[4*x+1][4*y +3] == ply:
				cnt_ply +=1

			elif bs[4*x+1][4*y +3]  == '-':
				cnt_dash +=1	

			else:
				return 0

			if cnt_ply == 4:
				return 16*(1 if ply == 'x' else -1)

			return cnt_ply

		elif ind == 3:

			#diamond 3
			cnt_ply = 0
			cnt_dash = 0

			if bs[4*x+2][4*y] == ply:
				cnt_ply +=1

			elif bs[4*x+2][4*y] == '-':
				cnt_dash +=1
			
			else:
				return 0

			if bs[4*x+1][4*y +1] == ply:
				cnt_ply +=1

			elif bs[4*x+1][4*y + 1] == '-':
				cnt_dash +=1	

			else:
				return 0

			if bs[4*x+3][4*y +1] == ply:
				cnt_ply +=1

			elif bs[4*x+3][4*y +1]  == '-':
				cnt_dash +=1

			else:
				return 0

			if bs[4*x+2][4*y +2] == ply:
				cnt_ply +=1

			elif bs[4*x+2][4*y +2]  == '-':
				cnt_dash +=1	

			else:
				return 0

			if cnt_ply == 4:
				return 16*(1 if ply == 'x' else -1)

			return cnt_ply
		#diamond 4
		elif ind == 4:
			cnt_ply = 0
			cnt_dash = 0

			if bs[4*x+2][4*y+1] == ply:
				cnt_ply +=1

			elif bs[4*x+2][4*y+1] == '-':
				cnt_dash +=1
			
			else:
				return 0

			if bs[4*x+1][4*y +2] == ply:
				cnt_ply +=1

			elif bs[4*x+1][4*y+2] == '-':
				cnt_dash +=1	

			else:
				return 0

			if bs[4*x+3][4*y +2] == ply:
				cnt_ply +=1

			elif bs[4*x+3][4*y +2]  == '-':
				cnt_dash +=1

			else:
				return 0

			if bs[4*x+2][4*y +3] == ply:
				cnt_ply +=1

			elif bs[4*x+2][4*y +3]  == '-':
				cnt_dash +=1	

			else:
				return 0

			if cnt_ply == 4:
				return 16*(1 if ply == 'x' else -1)

			return cnt_ply

		
		print("Invalid Ind")
	def block_check_diamond(self,ind,ply):
		bs = self.board.block_status
		if ind == 1:	
			#checking for diamond pattern
			#diamond 1
			cnt_ply = 0
			cnt_dash = 0

			if bs[0+1][0] == ply:
				cnt_ply +=1

			elif bs[0+1][0] == '-':
				cnt_dash +=1
		
			else:
				return 0

			if bs[0][0 +1] == ply:
				cnt_ply +=1

			elif bs[0][0 + 1] == '-':
				cnt_dash +=1	

			else:
				return 0
		

			if bs[0+2][0 +1] == ply:
				cnt_ply +=1

			elif bs[0+2][0 +1]  == '-':
				cnt_dash +=1

			else:
				return 0


			if bs[0+1][0 +2] == ply:
				cnt_ply +=1

			elif bs[0+1][0 +2]  == '-':
				cnt_dash +=1	

			else:
				return 0 

			if cnt_ply == 4:
				return 16*(1 if ply == 'x' else -1)

			return cnt_ply		

		elif ind == 2:	
			#diamond 2
			cnt_ply = 0
			cnt_dash = 0

			if bs[0+1][0+1] == ply:
				cnt_ply +=1

			elif bs[0+1][0+1] == '-':
				cnt_dash +=1
			
			else:
				return 0

			if bs[0][0+2] == ply:
				cnt_ply +=1

			elif bs[0][0+2] == '-':
				cnt_dash +=1	

			else:
				return 0

			if bs[0+2][0 +2] == ply:
				cnt_ply +=1

			elif bs[0+2][0 +2]  == '-':
				cnt_dash +=1

			else:
				return 0

			if bs[0+1][0 +3] == ply:
				cnt_ply +=1

			elif bs[0+1][0 +3]  == '-':
				cnt_dash +=1	

			else:
				return 0

			if cnt_ply == 4:
				return 16*(1 if ply == 'x' else -1)

			return cnt_ply

		elif ind == 3:

			#diamond 3
			cnt_ply = 0
			cnt_dash = 0

			if bs[0+2][0] == ply:
				cnt_ply +=1

			elif bs[0+2][0] == '-':
				cnt_dash +=1
			
			else:
				return 0

			if bs[0+1][0 +1] == ply:
				cnt_ply +=1

			elif bs[0+1][0 + 1] == '-':
				cnt_dash +=1	

			else:
				return 0

			if bs[0+3][0 +1] == ply:
				cnt_ply +=1

			elif bs[0+3][0 +1]  == '-':
				cnt_dash +=1

			else:
				return 0

			if bs[0+2][0 +2] == ply:
				cnt_ply +=1

			elif bs[0+2][0 +2]  == '-':
				cnt_dash +=1	

			else:
				return 0

			if cnt_ply == 4:
				return 16*(1 if ply == 'x' else -1)

			return cnt_ply
		#diamond 4
		elif ind == 4:
			cnt_ply = 0
			cnt_dash = 0

			if bs[0+2][0+1] == ply:
				cnt_ply +=1

			elif bs[0+2][0+1] == '-':
				cnt_dash +=1
			
			else:
				return 0

			if bs[0+1][0 +2] == ply:
				cnt_ply +=1

			elif bs[0+1][0+2] == '-':
				cnt_dash +=1	

			else:
				return 0

			if bs[0+3][0 +2] == ply:
				cnt_ply +=1

			elif bs[0+3][0 +2]  == '-':
				cnt_dash +=1

			else:
				return 0

			if bs[0+2][0 +3] == ply:
				cnt_ply +=1

			elif bs[0+2][0 +3]  == '-':
				cnt_dash +=1	

			else:
				return 0

			if cnt_ply == 4:
				return 16*(1 if ply == 'x' else -1)

			return cnt_ply

		
		print("Invalid Ind")


	def policy(self,possible_moves,ply):
		bs = self.board
		board_value = []
		print("Policy")

		for move in possible_moves:
			bs.board_status[move[0]][move[1]] = 'x' if ply == 1 else 'o'

			block_won	= self.check_block_status(move[0]/4,move[1]/4,'x' if ply == 1 else 'o') 

			if block_won == 1:
				bs.block_status[move[0]/4][move[1]/4] = 'o'

			elif block_won == 0:
				bs.block_status[move[0]/4][move[1]/4] = 'd'

			board_value.append(self.eval_board())


			if block_won != -1:
				bs.block_status[move[0]/4][move[1]/4] = '-'
		
			bs.board_status[move[0]][move[1]] = 'x' if ply == 1 else 'o'


		# print(possible_moves)
		# print(board_value)
		alpha = -1 if ply == 1 else 1

		index_array = sorted(range(len(board_value)), key = lambda r:board_value[r] )
		possible_moves = [possible_moves[alpha*i] for i in index_array ]

		# print(possible_moves)

		return possible_moves