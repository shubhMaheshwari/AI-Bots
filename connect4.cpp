//This a Connect4 Game (1-2 Player)
//Play this game by just compiling the programme and running it
//If you have any ideas to improve the quality of the game (especially the single player)
//please raise an issue 

#include <bits/stdc++.h> 
using namespace std;

char board[10][30],boardoriginal[10][30]=
    {"                         \0",
     "                         \0",
	 "|   |   |   |   |   |   |\0",
	 "|   |   |   |   |   |   |\0",
	 "|   |   |   |   |   |   |\0",
	 "|   |   |   |   |   |   |\0",
	 "|   |   |   |   |   |   |\0",
	 "|   |   |   |   |   |   |\0",
	 "|___|___|___|___|___|___|\0",
	 "  1   2   3   4   5   6  \0"},
	
	player[2][50]={{},"Computer"},wexit[5],score[10][105],single[5];
int a,b,place[7][6],centerx[6],centery[7],boardposition[2],totalscore[2],height[6],level=5;
//a,b are strlen of players
//place stores -1 ,1,0 to show what is played ' ' or 'X' or '0'
//center give the co-ordinate of the board 
//boardposition is the co-oridinate of the scoreboard to display board 	


//to display the board whenever needed
void displayboard()
{
	printf("\n\n");
	for (int i= 0; i< 10; i++)
		printf("%s 		%s\n",board[i],score[i]);
	printf("\n\n");
}

void instructions()
{
	printf("How to play\n");
	printf("1.Add X or 0 at diffrent Positions buy dropping into any of the 6 vertical blocks\n");
	printf("2.First person to make 4 consecutive horizontal vertical or diagonal X or 0 wins\n\n");
	printf("3.Winner gets 10 points\n  Loser get -5 points\n");
	printf("4.X playes first\n");
	printf("5.If X loses the players change\n");
	printf("6.Input -1 for hint\n");
	printf("Thank you for playing!!\n");

	printf("\n");
	for (int i= 0; i< 10; i++)
		printf("%s\n",boardoriginal[i]);
	printf("\n\n");
}

void initilize()
{

	for (int i = 0; i <6; ++i)	
		{height[i]=0;
		for (int j = 0; j <7; ++j)
			place[j][i]=-1;
		}
	
	for (int i = 0; i < 6; ++i)
		centerx[i]=2+4*i; 
			
	for (int j = 0; j < 7; j++)
		centery[j]=8-j;

	for (int i = 0; i < 10; ++i)
		for (int j = 0; j < 30; ++j)
			board[i][j]=boardoriginal[i][j];

}

void initilizeplayers()
{

a=strlen(player[1]);
b=strlen(player[0]);

//lines
score[0][0]=' ';
score[8][0]='|';
score[9][0]=' ';
for (int i = 1; i <b+a+6; ++i)
	{score[0][i]=score[8][i]='_';score[9][i]=' ';}
score[0][b+a+6]=' ';
score[8][6+a+b]='|';
score[8][3+a]='|';
score[9][3+a]='|';
score[0][a+b+7]=score[8][7+a+b]=score[9][7+a+b]='\0';

// name line
score[1][0]='|';
score[1][1]=' ';
for (int i = 0; i <a ; ++i)
	score[1][2+i]=player[1][i];
score[1][2+a]=' ';
score[1][3+a]='|';
score[1][4+a]=' ';
for (int i = 0; i < b; ++i)
	score[1][5+a+i]=player[0][i];
score[1][5+a+b]=' ';
score[1][6+a+b]='|';
score[1][7+a+b]='\0';

//scoreboard
for (int i = 2; i <8; ++i)
{
	score[i][0]='|';
	for (int j = 0; j <a+2 ; ++j)
		score[i][1+j]=' ';
	score[i][3+a]='|';
	for (int j = 0; j < b+2; ++j)
		score[i][4+a+j]=' ';
	score[i][6+a+b]='|';
	score[i][7+a+b]='\0';
}

boardposition[1]=2+a/2;
boardposition[0]=5+a+b/2;
totalscore[1]=0;
totalscore[0]=0;
score[9][boardposition[1]]='0';
score[9][boardposition[0]]='0';

}

void changescoreboard(int y,int x,int value)
{
	if (value==0)
	{
		score[y][x]='0';
		return;
	}

	else if(value<0)
	{
		score[y][x-1]='-';
		int digits=0;
		int temp=-1*value;
		for(;temp>0;)
			{temp/=10;digits++;}
		changescoreboard(y,x+digits-1,-1*value);
		return;
	}

	for(;value>0;x--)
		{score[y][x]='0'+value%10;value/=10;}

}

//changes the score on the scoreboard
void showscore(int isX,int level,int winner)
{
	if(winner==-1)
		score[level][boardposition[1]]=score[level][boardposition[0]]='0';
	
	else
	{
		if(isX==1)
		{
			changescoreboard(level,boardposition[winner],10);
			changescoreboard(level,boardposition[1-winner],-5);
			totalscore[winner]+=10;
			totalscore[1-winner]-=5;
			
			for (int i = -2; i <3 ; ++i)
				score[9][boardposition[1]+i]=' ';

			for (int i = -2; i <3 && boardposition[0]+i < 6 + a+b; ++i)
				score[9][boardposition[0]+i]=' ';
			
			changescoreboard(9,boardposition[winner],totalscore[winner]);
			changescoreboard(9,boardposition[1-winner],totalscore[1-winner]);
		}

	
		else
		{
			changescoreboard(level,boardposition[1-winner],10);
			changescoreboard(level,boardposition[winner],-5);
			totalscore[1-winner]+=10;
			totalscore[winner]-=5;
			
			for (int i = -2; i <3 ; ++i)
				score[9][boardposition[1]+i]=' ';

			for (int i = -2; i <3 && boardposition[0]+i < 6 + a+b; ++i)
				score[9][boardposition[0]+i]=' ';
			
			changescoreboard(9,boardposition[1-winner],totalscore[1-winner]);
			changescoreboard(9,boardposition[winner],totalscore[winner]);
		}

	}
}

//play on the board
void play(int player,int position)
{
if(place[height[position]][position]!=-1)
	{printf("Wrong position:%d\n",position);return;}

place[height[position]][position]=player;
board[centery[height[position]]][centerx[position]]=player?'X':'0';
}

//check if you win in this direction
int checker(int position,int dirx,int diry)
{
	if(dirx==0&&diry==0)
		return 0;

	int x=position,y=height[position];
	
	bool checkbet[4];
	//if you have a better way to do this please help!
	
	if(x+1*dirx > 5 || x+1*dirx < 0 || y+1*diry > 6 || y+1*diry < 0)
		checkbet[1]=false;
	else
		checkbet[1]=(place[y][x]==place[y+1*diry][x+1*dirx]);

	if(x+2*dirx > 5 || x+2*dirx < 0 || y+2*diry > 6 || y+2*diry < 0)
		checkbet[2]=false;
	else		
		checkbet[2]=(place[y][x]==place[y+2*diry][x+2*dirx]);

	if(x+3*dirx > 5 || x+3*dirx < 0 || y+3*diry > 6 || y+3*diry < 0)
		checkbet[3]=false;
	else		
		checkbet[3]=(place[y][x]==place[y+3*diry][x+3*dirx]);

	if(x-1*dirx > 5 || x-1*dirx < 0 || y-1*diry > 6 || y-1*diry < 0)
		checkbet[0]=false;
	else
		checkbet[0]=(place[y][x]==place[y-1*diry][x-1*dirx]);

	if(checkbet[1]&&checkbet[2]&&(checkbet[3]||checkbet[0]))
		return 50;

	return 0;
}

//check if someone won
int gameover(int position)
{
	int boardValue=0;
	for (int i = -1; i <2; ++i)
	for (int j = -1; j <2; ++j)
			boardValue+=checker(position,i,j);
	return boardValue;
}


//for the computer to make the right decision
int minmax(int isX,int depth,int initialDepth,int position,int alpha,int beta)
{
	place[height[position]][position]=isX;
	int valueOfBoard=gameover(position);

	if(valueOfBoard!=0)
	{
		place[height[position]][position]=-1;
		return (isX?1:-1)*(valueOfBoard-depth);
	}

	if(depth==level+initialDepth)
	{
		place[height[position]][position]=-1;
		return 0;
	}

	height[position]++;	
	int best,value;
	
	if(isX)
	{
		best=100;
		for (int i = 0; i<6; ++i)
		if(height[i]<7)
			{
				value=minmax(0,depth+1,initialDepth,i,alpha,beta);
				best = min(best,value);
				beta=min(best,beta);
				
				if(beta<=alpha)
					break;

			}	
	}

	else
	{
		best=-100;
		for (int i = 0; i<6; ++i)
		if(height[i]<7)
			{
				value=minmax(true,depth+1,initialDepth,i,alpha,beta);
				best=max(best,value);
				alpha=max(alpha,best);

				if(beta<=alpha)
					break;
			}
	}

	height[position]--;
	place[height[position]][position]=-1;	
	
	return best;
}

int computermove(int isX,int depth)
{ 
	int bestMove,bestValue=isX?-500:500,value;
	for (int i = 0; i < 6; ++i)
	if(height[i]<7)
		{
			value=minmax(isX,depth,depth,i,-1000,1000);
			printf("i:%d value:%d\n",i+1,value);
			if((bestValue<value&&isX)||(bestValue>value&&!isX))
				{
				bestValue=value;
				bestMove=i;
				}

		}

		printf("bestMove:%d\n",bestMove+1);
	return bestMove+1;
}


int main(int argc, char const *argv[])
{
	printf("\n\nCONNECT 4(2 Player)\n\n");
	instructions();
 
	printf("Single Player or Double Player?(Single-Double)\n");
	scanf("%s",single);

	if(single[0]!='S')
	{		
		printf("Enter Player X name\n");
		scanf("%s",player[1]);
	}	

 	int isX=1; //to check if  the person who was X in the start is still X
 	
	printf("Enter Player 0 name\n");
	scanf("%s",player[0]);

	initilizeplayers();

	bool flag=false;

	for (int start = 1;start<=7; ++start)
	{
	 	initilize();	
	 	printf("---Round :%d---\n",start);	
		displayboard();	 

		for (int i = 1; i <=42; ++i)	
		{
			int position;
	
			if(single[0]=='S'&&i%2==isX)
				position=computermove(isX,i);

			else
			{
				printf("Player%c:%s Enter The place to play(1-6)\n",i%2==0?'0':'X',player[i%2]);

				while(1)
				{ 
					scanf("%d",&position);
					if(position==-1)
						{printf("You should play at:%d\n",computermove(i%2,i));continue;}
					if(position>6|position<1)
						printf("Enter a digit between 1 and 6\n");
					else if(height[position-1]>6)
						printf("Column is filled\n");
					else if(place[height[position-1]][position-1]!=-1)
						printf("Something wrong with system\n");
					else
						break;

					printf("try again\n");
				}
			}


			play(i%2,position-1);
			//increment the height where the next player can play			
			if(gameover(position-1))
			{
				printf("     Player%c Won This Round \n",i%2==0?'0':'X');
				printf("     Congrats %s\n",player[i%2]);			
				showscore(isX,start+1,i%2);
				displayboard();
				//if 0 wins player change				
				if(single[0]=='S')
					{if((isX&&i%2==0)||(!isX&&i%2==1))
					{
						level+=10;
						printf("Level of Computer increased to %d\n",level);
					}}


				if(i%2==0)
					isX=1-isX;
				break;		
			
			}
			
			else if(i==42)
			{
			printf("     Its a Draw\n");
			showscore(isX,start+1,-1);
			}

			height[position-1]++;
			displayboard();

		}

		if(start<7)
		{printf("Do you want to continue?(yes or no)\n");
		scanf("%s",wexit);
		if(wexit[0]=='n')
			break;
		}

		else
		{
			printf("\n\nTournament is over\n\n");
			if(totalscore[1]==totalscore[0])
			printf("Its a draw\n");
			else
			printf("Winner is %s!!\n",player[totalscore[1]>totalscore[0]?1:0]);
		}

	}


	return 0;
}