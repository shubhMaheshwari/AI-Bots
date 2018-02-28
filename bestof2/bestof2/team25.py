from __future__ import print_function
import copy
import random
import datetime

class Team25():

	def __init__(self):

		self.INFINITY = 1e10
		self.termVal = self.INFINITY
		self.timeLimit = datetime.timedelta(seconds = 15.5)
		self.depth = 5
		self.weight = [4,2,2,4 ,2,3,3,2 ,2,3,3,2, 4,2,2,4]
		self.ply_value = {'x':1,'o':-1,'-':0,'d':0}
		self.trans = {}
		self.begin = self.INFINITY
		self.depthReach = 0
		self.board = ''

	def evaluate(self,blx,bly,tmpBlock):

		val = 0
		bs = self.board

		dimCnt = [10,10,10,10]
		dimCnt[0],val = self.check_diamond(4*blx+1,4*bly+1,dimCnt[0],val)
		dimCnt[1],val = self.check_diamond(4*blx+1,4*bly+2,dimCnt[1],val)
		dimCnt[2],val = self.check_diamond(4*blx+2,4*bly+1,dimCnt[2],val)
		dimCnt[3],val = self.check_diamond(4*blx+2,4*bly+2,dimCnt[3],val)

		rowCnt = [10,10,10,10]
		colCnt = [10,10,10,10]
		for i in xrange(4):
			for j in xrange(4):
				mark = bs.board_status[4*blx+i][4*bly+j]
				dictVal = self.ply_value[mark]
				if(dictVal==0):
					continue
				else:	
					val+=dictVal*self.weight[4*i+j]
					if (rowCnt[i]==10):
						rowCnt[i] = dictVal*5
					elif(dictVal*rowCnt[i]<0):
						rowCnt[i] = 0
					rowCnt[i]=rowCnt[i]*16
					if (colCnt[j]==10):
						colCnt[j] = dictVal*5
					elif(dictVal*colCnt[j]<0):
						colCnt[j] = 0
					colCnt[j]=colCnt[j]*16

		draw = 10
		for i in xrange(4):
			if(rowCnt[i]==0):
				draw-=1
			if(colCnt[i]==0):
				draw-=1
				

		if(draw==0):
			tmpBlock[blx][bly] = 'd'
			return 0



		for i in xrange(4):
			if(dimCnt[i]!=10):
				val+=dimCnt[i]

			if(rowCnt[i]!=10):
				val+=rowCnt[i]
			if(colCnt[i]!=10):
				val+=colCnt[i]
				

		return val

	def blockEval(self,tmpBlock):

		val = 0
		
		dimCnt,val = self.block_check_diamond(tmpBlock,val)

		rowCnt = [10,10,10,10]
		colCnt = [10,10,10,10]
		for i in xrange(4):
			for j in xrange(4):
				mark = tmpBlock[i][j]
				dictVal = self.ply_value[mark]
				if dictVal == 0:
					continue

				else:
					val+=dictVal*self.weight[4*i+j]
					if (rowCnt[i]==10):
						rowCnt[i] = dictVal*5
					elif(dictVal*rowCnt[i]<=0):
						rowCnt[i] = 0
					rowCnt[i]=rowCnt[i]*16
					if (colCnt[j]==10):
						colCnt[j] = dictVal*5
					elif(dictVal*colCnt[j]<=0):
						colCnt[j] = 0
					colCnt[j]=colCnt[j]*16



		for i in xrange(4):
			if(rowCnt[i]!=10):
				val+=rowCnt[i]
			if(colCnt[i]!=10):
				val+=colCnt[i]
			if(dimCnt[i]!=10):
				val+=dimCnt[i]	


		return val

	def heuristic(self):
		bs = self.board
		tmpBlock = copy.deepcopy(bs.block_status)
		final = 0
		for i in xrange(4):
			for j in xrange(4):
				b_value = self.evaluate(i,j,tmpBlock)
				final += b_value
		final += self.blockEval(tmpBlock)*120
		del(tmpBlock)
		return final

	def minimax(self,  old_move, flag, depth, alpha, beta):
		board = self.board

		hashval = hash(str(board.board_status))
		if(self.trans.has_key(hashval)):
			# print("hash exists")
			bounds = self.trans[hashval]
			if(bounds[0] >= beta):
				return bounds[0],old_move
			if(bounds[1] <= alpha):
				return bounds[1],old_move
			# print("also returning")
			alpha = max(alpha,bounds[0])
			beta = min(beta,bounds[1])

		cells = board.find_valid_move_cells(old_move)
		random.shuffle(cells)
		# print(len(cells), ": length of cells")
		if (flag == 'x'):
			nodeVal = -self.INFINITY, cells[0]
			new = 'o'
			tmp = copy.deepcopy(board.block_status)
			a = alpha

			for chosen in cells :
				if datetime.datetime.utcnow() - self.begin >= self.timeLimit :
					# print("breaking at depth ",depth)
					self.depthReach = 1
					break
				board.update(old_move, chosen, flag)
				# print("chosen ",chosen)
				if (board.find_terminal_state()[0] == 'x'):
					board.board_status[chosen[0]][chosen[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					nodeVal = self.termVal,chosen
					break
				elif (board.find_terminal_state()[0] == 'o'):
					board.board_status[chosen[0]][chosen[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					continue
				elif(board.find_terminal_state()[0] == 'NONE'):
					# print("entering")
					x = 0
					d = 0
					o = 0
					tmp1 = 0
					# print("initialized")
					for i2 in xrange(4):
						for j2 in xrange(4):
							if(board.block_status[i2][j2] == 'x'):
								x += 1
							if(board.block_status[i2][j2] == 'o'):
								o += 1
							if(board.block_status[i2][j2] == 'd'):
								d += 1
					# print("counted")
					if(x==o):
						tmp1 = 0
					elif(x>o):
						tmp1 = self.INFINITY/2 + 10*(x-o)
					else:
						tmp1 = -self.INFINITY/2 - 10*(o-x)
					# print(tmp1)
				elif( depth >= self.depth):
					tmp1 = self.heuristic()
					# print("Heuristic value for ",chosen," is ",tmp1)
				else:
					tmp1 = self.minimax( chosen, new, depth+1, a, beta)[0]

				board.board_status[chosen[0]][chosen[1]] = '-'
				board.block_status = copy.deepcopy(tmp)
				if(nodeVal[0] < tmp1):
					nodeVal = tmp1,chosen
				# print("hi nodeval ",nodeVal)
				a = max(a, tmp1)
				if beta <= nodeVal[0] :
					break
			del(tmp)

		if (flag == 'o'):
			nodeVal = self.INFINITY, cells[0]
			new = 'x'
			tmp = copy.deepcopy(board.block_status)
			b = beta

			for chosen in cells :
				if datetime.datetime.utcnow() - self.begin >= self.timeLimit :
					# print("breaking")
					self.depthReach = 1
					break
				board.update(old_move, chosen, flag)
				# print("chosen ",chosen)
				if(board.find_terminal_state()[0] == 'o'):
					board.board_status[chosen[0]][chosen[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					nodeVal = -1*self.termVal,chosen
					break
				elif(board.find_terminal_state()[0] == 'x'):
					board.board_status[chosen[0]][chosen[1]] = '-'
					board.block_status = copy.deepcopy(tmp)
					continue
				elif(board.find_terminal_state()[0] == 'NONE'):
					# xprint("entering")
					x = 0
					d = 0
					o = 0
					tmp1 = 0
					# print("initialized")
					for i2 in range(4):
						for j2 in range(4):
							if board.block_status[i2][j2] == 'x':
								x += 1
							if board.block_status[i2][j2] == 'o':
								o += 1
							if board.block_status[i2][j2] == 'd':
								d += 1
					# print("counted")
					if(x==o):
						tmp1 = 0
					elif(x>o):
						tmp1 = self.INFINITY/2 + 10*(x-o)
					else:
						tmp1 = -self.INFINITY/2 - 10*(o-x)
					# print(tmp1)
				elif(depth >= self.depth):
					tmp1 = self.heuristic()
					# print("Heuristic value for ",chosen," is ",tmp1)
				else:
					tmp1 = self.minimax( chosen, new, depth+1, alpha, b)[0]
				board.board_status[chosen[0]][chosen[1]] = '-'
				board.block_status = copy.deepcopy(tmp)
				if(nodeVal[0] > tmp1):
					nodeVal = tmp1,chosen
				b = min(b, tmp1)
				if alpha >= nodeVal[0] :
					break
			del(tmp)

		# print("return value is ",nodeVal)
		if(nodeVal[0] <= alpha):
			self.trans[hashval] = [-self.INFINITY,nodeVal[0]]
		if(nodeVal[0] > alpha and nodeVal[0] < beta):
			self.trans[hashval] = [nodeVal[0],nodeVal[0]]
		if(nodeVal[0]>=beta):
			self.trans[hashval] = [nodeVal[0],self.INFINITY]
		# print(self.trans.items())
		return nodeVal			
		
	def move(self, board, old_move, flag):
		self.begin = datetime.datetime.utcnow()
		self.depthReach = 0
		self.trans.clear()
		self.board = copy.deepcopy(board)

		sub_val= 0
		for i in xrange(3,100):
			self.trans.clear()
			self.depth = i


			sub_val,sub_move = self.minimax(old_move,flag,1, -self.INFINITY, self.INFINITY)

			if(self.depthReach == 0):
				move = sub_move
			else:
				break

		return move

	def check_diamond(self,blx,bly,dimCnt,val):

		bs = self.board

		for i,j in [(0,1) , (1,0) , (-1,0) , (0,-1)]:
			mark = bs.board_status[blx+i][bly+j]
			dictVal = self.ply_value[mark]
			if(dictVal ==0):
				continue
			else:	
				val+=dictVal*self.weight[4*i+j]
				if (dimCnt ==10):
					dimCnt  = dictVal*5
				elif(dictVal*dimCnt <0):
					dimCnt  = 0
				dimCnt =dimCnt *16

		return dimCnt,val		

	def block_check_diamond(self,tmpBlock,val):

		dimCnt = [10,10,10,10]
		for ind,elem in enumerate([(1,1) , (1,2) , (2,1) , (2,2)]):
			k,l = elem
			for i,j in [(0,1) , (1,0) , (-1,0) , (0,-1)]:	
				mark = tmpBlock[k + i][l + j]
				dictVal = self.ply_value[mark]
				if dictVal == 0:
					continue
				else:	
					val+=dictVal*self.weight[4*(i+k) + j+l]
					dictVal = self.ply_value[mark]
					if(dimCnt[ind]==10):
						dimCnt[ind] = dictVal*5
					elif(dictVal*dimCnt[ind]<=0):
						dimCnt[ind] = 0
					dimCnt[ind]=dimCnt[ind]*16*dictVal*dictVal

		return dimCnt,val			