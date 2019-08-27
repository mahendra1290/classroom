#include<stdio.h>
#include<string.h>
#include <math.h>

char X = 'X';
char O = 'O';
char Empty = '.';

int isValid(int xCount, int oCount);
char checkRow(int row, char str[3][3]);
char checkCol(int col, char str[3][3]);
char checkDiag(int diag, char str[3][3]);
int checkRowWise(char str[3][3]);

int main()
{
    int i,j,emptyCount=0,Blnk,xCount=0,oCount=0;
    char str[3][3];
    for(int i = 0; i < 3; i++){
        scanf("%s",&str[i]);
    }
    for(int i = 0;i < 3; i++){
        for(int j = 0; j < 3; j++){
            printf("%c\n", str[i][j]);
            if(str[i][j] == X){
                xCount++;
            }
            else if(str[i][j] == O){
                oCount++;
            }
            else{
                emptyCount++;
            }
        }
    }
    // if (!isValid(xCount, oCount)){
    //     printf("Wait, what?\n");
    // }
    // else if(checkDiag == 1){
    //     printf
    // }
    printf("x = %d , o = %d, e = %d\n", xCount, oCount, emptyCount);
    printf("diag_1 = %c\n", checkDiag(1, str));
    printf("diag_2 = %c\n", checkDiag(2, str));
 
}

int checkRowWise(char str[3][3]){
    int count = 0;
    for (int i = 0; i < 3; i++){
        if(checkRow(i, str) != '-'){
            count++;
        }
    }
    return count;
}

int checkColWise(char str[3][3]){
    int count = 0;
    for (int i = 0; i < 3; i++){
        if(checkCol(i, str) != '-'){
            count++;
        }
    }
    return count;
}

int checkDiagWise(char str[3][3]){
    for (int i = 1; i < 3; i++){
        if (checkDiag(i, str) != '-'){
            return 1;
        }
    }
    return 0;
}

char checkRow(int row, char str[3][3]){
    int i;
    char score = str[row][0];
    for (i = 0; i < 3; i++){
        if ( (score != str[row][i]) || score == '.'){
            break;
        }
    }
    if (i != 3){
        score = '-';
    }
    return score;
}

char checkCol(int col, char str[3][3]){
    int i;
    char score = str[0][col];
    for (i = 0; i < 3; i++){
        if ( (score != str[i][col]) || score == '.'){
            break;
        }
    }
    if (i != 3){
        score = '-';
    }
    return score;
    //jijij
}

char checkDiag(int diag, char str[3][3]){
    int next = 0;
    int i;
    if (diag == 2){
        next = 2;
    }
    char score = str[0][next];
    for (i = 0; i < 3; i++){
        int j = abs(next - i);
        if ((str[i][j] != score) || score == '.'){
            return '-';
        }
    }
    return score;
}

int isValid(int xCount, int oCount){
    if (oCount > xCount){
        return 0;
    }
    else if( (xCount - oCount) > 1){
        return 0;
    }
    return 1;
}