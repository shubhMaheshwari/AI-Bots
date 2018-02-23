import sys
import random
import signal
import time
import copy
import json	


import numpy as np
TIME = 32
MAX_PTS = 68
# N = 4
t2 = 0 
t1 = 0
training_data = []
# For min max with pruning 
# turn depth num win lost draw
# 180  4	 10   5   2    3	
# 160  4	 10   4   2    4	
# 160  5	 10   3   0    7	
# 100  30	 10   4   0    6	
# 100  30	 10   4   0    6	
#  0   30	 10   5   2    3	
#  50   30	 10   4   1    5	

class Simple_minimax(object):

	def __init__(self, ply):
		self.ply = 1 if ply == 'x' else -1
		self.board = ''	
		self.turn = 0 if ply == 'x' else 1
		pass


	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		# print("Allowed moves:",possible_moves)
		self.board = copy.deepcopy(board)
		# print("Current Board state")
		# self.board.print_board()
		# IDA instead of DFS

		# for i in range(1,self.turn):

		self.turn += 2
		if self.turn < 9:
			possible_moves = self.board.find_valid_move_cells()
			return random.sample(possible_moves, 1)[0]
		sub_move,move_value = self.min_max(old_move,self.ply)
		print("move:",sub_move,"value:",move_value,"ply:",self.ply)
	

		return sub_move	

	def min_max(self, old_move,ply,alpha = -10000,beta = 10000,depth=0):		

		# print(-1*ply,old_move)
		bs = self.board 		
		# bs.print_board()
		# print("old move:",old_move)
		winner, message = bs.find_terminal_state()


		# print("winner:",winner,"message:",message)
		if message == 'WON':
			return old_move,-ply*(16-depth)
		elif message == 'DRAW':
			return old_move,0
		possible_moves = bs.find_valid_move_cells()

		# print(possible_moves)
		best_move = ''
		best_val = -100*ply

		for move in possible_moves:
			# print(possible_moves)

			bs.block_status[move[0]][move[1]] = 'x' if ply == 1 else 'o'
			sub_move, sub_value = self.min_max(move, -1*ply,alpha,beta,depth+1)
			# print("sub_value",sub_value)

			if ply == 1:
				if sub_value > best_val:
						best_val = sub_value
						best_move = move

				alpha = max(alpha,best_val)


			elif ply == -1:
				if sub_value < best_val:
						best_val = sub_value
						best_move = move

				beta = min(beta,best_val)

			# print("alpha:",alpha,"beta",beta)
			bs.block_status[move[0]][move[1]] = '-'
	
			if(beta <= alpha):
				# print("Alpha beta prunned")
				break				


		return best_move, best_val


class RandomPlayer():
	# ply is the character x or o
	def __init__(self,ply):
		self.block_number = 0
		self.ply = ply
		pass

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		possible_moves = board.find_valid_move_cells()
		# udpate_list = [board.update(old_move,new_move,self.ply) for new_moves in possible_moves]
		# print possible_moves
		# print udpate_list
		return random.sample(possible_moves,1)[0]

class Manual_Player:
	def __init__(self):
		pass
	def move(self, board, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		cells = board.find_valid_move_cells()
		print 'Valid Moves'
		print cells
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))		


class TimedOutExc(Exception):
	pass

def handler(signum, frame):
	#print 'Signal handler called with signal', signum
	raise TimedOutExc()

class Board:

	def __init__(self):
		# board_status is the game board
		# block status shows which blocks have been won/drawn and by which player
		self.block_status = [['-' for i in range(4)] for j in range(4)]

	def print_board(self):
		# for printing the state of the board

		print '==============Block State=============='
		for i in range(4):
			for j in range(4):
				print self.block_status[i][j],
			print 
		print '======================================='
		print
		print

	# old move = (row,column) row,column = [0,15]
	def find_valid_move_cells(self):
		#returns the valid cells allowed given the last move and the current board state
		allowed_cells = []
		for i in range(4):
			for j in range(4):
				if self.block_status[i][j] == '-':
					allowed_cells.append((i,j))

		return allowed_cells	

	# check whether game is over or not 
	def find_terminal_state(self):
		#checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher blocks in case of a draw
		bs = self.block_status

		cntx = 0
		cnto = 0

		for i in range(4):						#counts the blocks won by x, o and drawn blocks
			for j in range(4):
				if bs[i][j] == 'x':
					cntx += 1
				if bs[i][j] == 'o':
					cnto += 1

		for i in range(4):
			row = bs[i]							#i'th row 
			col = [x[i] for x in bs]			#i'th column
			#print row,col
			#checking if i'th row or i'th column has been won or not
			if (row[0] =='x' or row[0] == 'o') and (row.count(row[0]) == 4):	
				# print("row:",i)
				return (row[0],'WON')
			if (col[0] =='x' or col[0] == 'o') and (col.count(col[0]) == 4):
				# print("col:",i)
				return (col[0],'WON')

		#checking if diamond has been won
		if(bs[1][0] == bs[0][1] == bs[2][1] == bs[1][2]) and (bs[1][0] == 'x' or bs[1][0] == 'o'):
			# print('dim:',1)
			return (bs[1][0],'WON')
		if(bs[1][1] == bs[0][2] == bs[2][2] == bs[1][3]) and (bs[1][1] == 'x' or bs[1][1] == 'o'):
			# print('dim:',2)
			return (bs[1][1],'WON')
		if(bs[2][0] == bs[1][1] == bs[3][1] == bs[2][2]) and (bs[2][0] == 'x' or bs[2][0] == 'o'):
			# print('dim:',3)			
			return (bs[2][0],'WON')
		if(bs[2][1] == bs[1][2] == bs[3][2] == bs[2][3]) and (bs[2][1] == 'x' or bs[2][1] == 'o'):
			# print('dim:',4)
			return (bs[2][1],'WON')

		if cntx+cnto <16:		#if all blocks have not yet been won, continue
			return ('-', 'CONTINUE')
		elif cntx+cnto == 16:							#if game is drawn
			return ('NONE', 'DRAW')

	def check_valid_move(self, old_move, new_move):
		#checks if a move is valid or not given the last move
		if (len(old_move) != 2) or (len(new_move) != 2):
			return False 
		if (type(old_move[0]) is not int) or (type(old_move[1]) is not int) or (type(new_move[0]) is not int) or (type(new_move[1]) is not int):
			return False
		

		if (old_move != (-1,-1)) and (old_move[0] < 0 or old_move[0] > 16 or old_move[1] < 0 or old_move[1] > 16):
			return False
		cells = self.find_valid_move_cells()

		return new_move in cells

	def update(self, old_move, new_move, ply):
		
		#updating the game board and block status as per the move that has been passed in the arguements
		if(self.check_valid_move(old_move, new_move)) == False:
			return 'UNSUCCESSFUL', False

		x = new_move[0]
		y = new_move[1]

		self.block_status[x][y] = ply

		return 'SUCCESSFUL', True

def player_turn(game_board, old_move, obj, ply, opp, flg,turn):
		
		global t2,t1

		# print("turn:",turn, "ply:",ply)
		temp_block_status = copy.deepcopy(game_board.block_status)
		signal.alarm(TIME)
		WINNER = ''
		MESSAGE = ''
		pts = {"P1" : 0, "P2" : 0}
		to_break = False
		p_move = old_move
		try:	
			#try to get player 1's move	
			t1 = time.time()
			p_move = obj.move(game_board, old_move, flg)
			t2 = time.time()
			print("Turn:",turn,"Time:",t2 - t1)

		except TimedOutExc:					#timeout error
#			print e
			WINNER = opp
			MESSAGE = 'TIME OUT'
			pts[opp] = MAX_PTS
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False,turn
		# except Exception as e:
		# 	exc_type, exc_obj, exc_tb = sys.exc_info()
		# 	print(exc_obj,exc_tb.tb_lineno)
		# 	WINNER = opp
		# 	MESSAGE = 'INVALID MOVE'
		# 	pts[opp] = MAX_PTS			
		# 	return old_move, WINNER, MESSAGE , pts["P1"], pts["P2"], False, False,turn
		# signal.alarm(0)

		#check if board is not modified and move returned is valid
		if  game_board.block_status != temp_block_status:
			WINNER = opp
			MESSAGE = 'MODIFIED THE BOARD'
			pts[opp] = MAX_PTS
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False,turn +1

		update_status = game_board.update(old_move, p_move, flg)
		# print("move played : ",p_move)
			
		if update_status == 'UNSUCCESSFUL':
			WINNER = opp
			MESSAGE = 'INVALID MOVE'
			pts[opp] = MAX_PTS
			print("Update UNSUCCESSFUL")
			exit()
			return old_move, WINNER, MESSAGE, pts["P1"], pts["P2"], False, False,turn

		status = game_board.find_terminal_state()		#find if the game has ended and if yes, find the winner
		if status[1] == 'WON':	
			#if the game has ended after a player1 move, player 1 would win
			print("Status for win:",status)			
			pts[ply] = MAX_PTS
			WINNER = ply
			MESSAGE = 'WON'
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False,turn
		elif status[1] == 'DRAW':						#in case of a draw, each player gets points equal to the number of blocks won
			WINNER = 'NONE'
			MESSAGE = 'DRAW'
			return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], True, False,turn

		return p_move, WINNER, MESSAGE, pts["P1"], pts["P2"], False, True, turn+1

def gameplay(obj1, obj2):				#game simulator
	global training_data
	game_board = Board()
	fl1 = 'x'
	fl2 = 'o'
	old_move = (-1,-1)
	WINNER = ''
	MESSAGE = ''	
	pts1 = 0
	pts2 = 0
	turn = 0

	# game_board.print_board()
	signal.signal(signal.SIGALRM, handler)
	while (turn < 16):
		p_move, WINNER, MESSAGE, pts1, pts2, to_break, block_won,turn = player_turn(game_board, old_move, obj1 if turn%2 == 0 else obj2, "P1" if turn%2 == 0 else "P2" , "P2" if turn%2 == 0 else "P1" , fl1 if turn%2 == 0 else fl2,turn)	

		# Stupid same memory is being used,hence we need a new variable

		if turn > 12:
			old_board = copy.deepcopy(game_board.block_status)
			x_train = {'board':old_board,
				'WINNER':WINNER,
				'old_move':old_move,
				}

			training_data.append(x_train)
			x_train = {}
			

		# print(p_move, WINNER, MESSAGE, pts1, pts2, to_break, block_won,turn)
		if to_break:
			break

		old_move = p_move
		game_board.print_board()

		# break
		# if turn > 5:
		# 	break	
		# #do the same thing for player 2
		# p2_move, WINNER, MESSAGE, pts1, pts2, to_break, block_won = player_turn(game_board, old_move, obj2, "P2", "P1", fl2)

		# if to_break:
		# 	break

		# game_board.print_board()
		# old_move = p2_move

		# if block_won:
		# 	p2_move, WINNER, MESSAGE, pts1, pts2, to_break, block_won = player_turn(game_board, old_move, obj2, "P2", "P1", fl2)
		
		# 	if to_break:
		# 		break
		
		# 	old_move = p2_move
		# 	game_board.print_board()
	game_board.print_board()

	print "Winner:", WINNER
	print "Message", MESSAGE

	x = 0
	d = 0
	o = 0
	for i in range(4):
		for j in range(4):
			if game_board.block_status[i][j] == 'x':
				x += 1
			if game_board.block_status[i][j] == 'o':
				o += 1
			if game_board.block_status[i][j] == 'd':
				d += 1
	print 'x:', x, ' o:',o,' d:',d
	if MESSAGE == 'DRAW':

	# After the game is over
		for i in range(4):
			for j in range(4):
				val = 4
				if is_corner(i,j):
					val = 6
				elif is_centre(i,j):
					val = 3
				if game_board.block_status[i][j] == 'x':
					pts1 += val
				if game_board.block_status[i][j] == 'o':
					pts2 += val
	return (pts1,pts2)

def is_centre(row, col):
	if row == 1 and col == 1:
		return 1
	if row == 1 and col == 2:
		return 1
	if row == 2 and col == 1:
		return 1
	if row == 2 and col == 2:
		return 1
	return 0

def is_corner(row, col):
	if row == 0 and col == 0:
		return 1
	if row == 0 and col == 3:
		return 1
	if row == 3 and col == 0:
		return 1
	if row == 3 and col == 3:
		return 1
	return 0


TURN_RAND_STOP = 30 # Stop random moves after move 50

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 	data = []
	saitama1 = ''
	saitama2 = ''
	option = sys.argv[1]	
	for i in range(3000):
		training_data = []
		if i%2 == 1:
			saitama1 = Simple_minimax('x')
			saitama2 = RandomPlayer('o')

		elif i%2 == 0:
			saitama1 = RandomPlayer('x')
			saitama2 = Simple_minimax('o')
		else:
			print 'Invalid option'
			sys.exit(1)

		saitama3 = RandomPlayer('x')
		try:
			x = gameplay(saitama1, saitama2)
			print "Player 1 points:", x[0] 
			print "Player 2 points:", x[1]
			print([x['board'] for x in training_data])
		except KeyboardInterrupt :
			break

		print i
		data.append(training_data)	
	

	r = open('simple_game.json','w+')
	# data = json.load(r)
	# data.update(training_data)
	json.dump(data, r)

	# saitama1 = Manual_Player()
	# saitama2 = Simple_minimax('o')

	# x = gameplay(saitama1, saitama2)
	# print "Player 1 points:", x[0] 
	# print "Player 2 points:", x[1]

