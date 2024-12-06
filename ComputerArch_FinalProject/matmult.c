#include <stdio.h>

#define NRA 60            /* number of rows in matrix A */
#define NCA 12            /* number of columns in matrix A */
#define NRB 12            /* number of rows in matrix B, should equal to NCA */
#define NCB 10            /* number of columns in matrix B */

int main (int argc, char *argv[]) {
    int A[NRA][NCA],      /* matrix A to be multiplied */
        B[NRB][NCB],      /* matrix B to be multiplied */
        C[NRA][NCB];      /* result matrix C */
    int i, j, k;          /* loop counters */

    // Do some basic error checking
    if (NRB != NCA) {
        printf("Matrix A column size must equal matrix B row size.\n");
        return 1;
    } 

    printf("Matrix A: #rows %d; #cols %d\n", NRA, NCA);
    printf("Matrix B: #rows %d; #cols %d\n", NRB, NCB);
    printf("\n");

    /* Initializing and printing matrix A */
    printf("Initializing matrix A...\n");
    for (i = 0; i < NRA; i++) {
        for (j = 0; j < NCA; j++) {
            A[i][j] = i + j;  /* A[i][j] = i + j */
        }
    }

    printf("Contents of matrix A\n");
    for (i = 0; i < NRA; i++) {
        for (j = 0; j < NCA; j++) {
            printf("%d\t", A[i][j]);
        }
        printf("\n");
    }

    /* Initializing and printing matrix B */
    printf("Initializing matrix B...\n");
    for (i = 0; i < NRB; i++) {
        for (j = 0; j < NCB; j++) {
            B[i][j] = i - j;  /* B[i][j] = i - j */
        }
    }

    printf("Contents of matrix B\n");
    for (i = 0; i < NRB; i++) {
        for (j = 0; j < NCB; j++) {
            printf("%d\t", B[i][j]);
        }
        printf("\n");
    }

    /* Calculate matrix multiplication results for C */
    printf("Calculating matrix multiplication...\n");
    for (i = 0; i < NRA; i++) {
        for (j = 0; j < NCB; j++) {
            C[i][j] = 0;
            for (k = 0; k < NCA; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    /* Print result matrix C */
    printf("\n");
    printf("******************************************************\n");
    printf("Result Matrix C:\n");
    for (i = 0; i < NRA; i++) {
        printf("\n");
        for (j = 0; j < NCB; j++) {
            printf("%d\t", C[i][j]);
        }
    }
    
    printf("\n******************************************************\n");
    printf("\n");

    return 0;
}
