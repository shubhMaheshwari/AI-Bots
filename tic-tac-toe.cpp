//This a  Tic-Tac-Toe Game (1-2 Player)
//Play this game by just compiling the programme and running it
//If you have any ideas to improve the quality of the game (especially the single player)
//please raise an issue 

#include <bits/stdc++.h>
using namespace std;

char board[12][25],boardoriginal[12][25]=
{" _________________ \0",
	 "|     |     |     |\0",
	 "|  1  |  2  |  3  |\0",
	 "|_____|_____|_____|\0",
	 "|     |     |     |\0",
	 "|  4  |  5  |  6  |\0",
	 "|_____|_____|_____|\0",
	 "|     |     |     |\0",
	 "|  7  |  8  |  9  |\0",
	 "|_____|_____|_____|\0"},
	player[2][50]={{},"Computer"},wexit[5],score[12][105],single[5];
int a,b,place[9],centerx[9],centery[9],boardposition[2],totalscore[2];
bool flag;

void displayboard()
{
	printf("\n");
	for (int i= 0; i< 10; i++)
		printf("%s 		%s\n",board[i],score[i]);
	printf("\n\n");
}

void instructions()
{
	printf("How to play\n");
	printf("1.Add X or 0 at diffrent Positions\n");

	printf("2.To Play at a Positions they numbered as\n");
	printf("\n");
	for (int i= 0; i< 10; i++)
		printf("%s\n",boardoriginal[i]);
	printf("\n\n");

	printf("3.Winner gets 10 points\n  Loser get -5 points\n");
	printf("4.X playes first\n");
	printf("5.If X loses the players change\n");
	printf("6.Input -1 for hint\n");
	printf("Thank you for playing!!\n\n\n");
}

void initilize()
{
	for (int i = 0; i <9; ++i)
		place[i]=-1;
	
	for (int i = 0; i < 3; ++i)
	{
		
		for (int j = 0; j < 3; j++)
			{
				centerx[i*3+j]=3+6*j; 
				centery[i*3+j]=2+3*i;
			}
	}

	for (int i = 0; i < 12; ++i)
		for (int j = 0; j < 25; ++j)
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

printf("%s\n",score[9]);

printf("\nScoreboard\n");
for (int i = 0; i <12 ; ++i)
	printf("%s\n",score[i]);
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


void play(int player,int position)
{
if(place[position]!=-1)
	{printf("Wrong position:%d\n",position);return;}

place[position]=player;
if(player==0)
{
	for (int i = -1; i <=1; ++i)
		for (int j = -1; j <=1; ++j)
			board[centery[position]+i][centerx[position]+j]='0';
	board[centery[position]][centerx[position]]='1'+position;
}	
	
else
{
	for (int i = -1; i <=1; i+=2)
		for (int j = -1; j <=1; j+=2)
			board[centery[position]+i][centerx[position]+j]='X';
}


}

bool gameover(int position)
{
	//check horizontal
	if(place[position]==place[3*(position/3)]&&place[position]==place[3*(position/3)+1]&&place[position]==place[3*(position/3)+2])
		return true;	
	//check vertical
	else if(place[position]==place[position%3]&&place[position]==place[3+position%3]&&place[position]==place[6+position%3])
		return true;
	//check diagonal
	if(position==0||position==2||position==4||position==6||position==8)
	{
		if(place[position]==place[0]&&place[position]==place[4]&&place[position]==place[8])
			return true;
		else if(place[position]==place[2]&&place[position]==place[4]&&place[position]==place[6])
			return true;
	}
	
	return false;
}

int minmax(bool isX,int depth,int position)
{
	place[position]=isX?1:0;

	if(gameover(position))
	{

		place[position]=-1;
		return (isX?1:-1)*(10-depth);
	}

	if(depth==9)
	{
		place[position]=-1;
		return 0;
	}

	int best,value;

	if(isX)
	{
		best=100;
		for (int i = 0; i<9; ++i)
		if(place[i]==-1)
			{
				value=minmax(false,depth+1,i);
				if(value==depth-9)
					{best=value;break;}
				else
					best=min(best,value);
			}
	
	}

	else
	{
		best=-100;
		for (int i = 0; i<9; ++i)
		if(place[i]==-1)
			{
				value=minmax(true,depth+1,i);
				if(value==9-depth)
					{best=value;break;}

				else
					best=max(best,value);
			}
	}

	place[position]=-1;	
	return best;
}


int computermove(bool isX,int depth)
{
	int bestMove,bestVal=isX?-100:100,value;
	
		for (int i = 0; i < 9; ++i)
			if(place[i]==-1)
				{
					value=minmax(isX,depth,i);
					printf("i:%d value:%d\n",i+1,value);
					if((bestVal<value&&isX)||(bestVal>value&&!isX))
						{
						bestVal=value;
						bestMove=i;
						}


				}
	
	return bestMove+1;
}


int main()
{	
	printf("\n\nTIC-TAC-TOE\n\n\n");
	instructions();
 

 	int isX; //to check if  the person who was X in the start is still X
	flag=false;
	printf("Single Player or Double Player?(Single-Double)\n");
	scanf("%s",single);

	if(single[0]!='S')
	{		
		printf("Enter Player 0 name\n");
		scanf("%s",player[1]);
	}

	isX=0;
 	
	printf("Enter Player X name\n");
	scanf("%s",player[0]);

	initilizeplayers();

	for (int start = 1;start<=7; ++start)
	{
	 	initilize();	
	 	printf("---Round :%d---\n",start);	
		 
		displayboard();

		for (int i = 1; i <=9; ++i)	
		{
			int position;
	
			if(single[0]=='S'&&i%2==isX)
				position=computermove(isX==1?true:false,i);

			else
			{
				printf("Player%c:%s Enter The place to play(1-9)\n",i%2==0?'0':'X',player[i%2]);

				flag=false;
				while(flag==false)
				{ 
					scanf("%d",&position);
					if(position==-1)
						{printf("You should play at:%d\n",computermove(i%2==1?true:false,i));continue;}
					if(position>9|position<1)
						printf("Enter a digit between 1 and 9\n");
					else if(place[position-1]!=-1)
						printf("The position is already taken\n");
					else
						break;

					printf("try again\n");
				}
				flag=false;
			}


			play(i%2,position-1);
			displayboard();
			
			if(gameover(position-1))
			{
				printf("     Player%c Won This Round \n",i%2==0?'0':'X');
				printf("     Congrats %s\n",player[i%2]);			
				showscore(isX,start+1,i%2);
				displayboard();
				//if 0 wins player change				
				if(i%2==0)
					isX=1-isX;
				break;		
			}
			
			else if(i==9)
			{
				
			printf("     Its a Draw\n");
			showscore(isX,start+1,-1);
			displayboard(); 			
			}

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
			if(totalscore[1]>totalscore[0])
			printf("Winner is %s!!\n",player[1]);
			else if(totalscore[1]==totalscore[0])
			printf("Its a draw\n");
			else
			printf("Winner is %s!!\n",player[0]);
		}

	}
	
	return 0;
}	