#include <stdio.h>
#include <stdlib.h>

int main() {
    int j=0, k=0, q[10], w[10];
    int n, m, s, temp;
    int arr[10];
    int a[10];
    int b[20];
    printf("enter no of elements:");
    scanf("%d", &n);
    // printf("enter no of elements:");
    // scanf("%d", &m);


    // initilaize array arr[10]
    for (int i = 0; i < n; i++)
    {
        scanf("%d", &arr[i]);
    }

    // initilaize array a[10]
    // for (int i = 0; i < m; i++)
    // {
    //     scanf("%d", &a[i]);
    // }

    // array display
    for (int i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }
    // printf("\n\n");

    // for (int i = 0; i < m; i++)
    // {
    //     printf("%d", a[i]);
    // }
    
    // printf("\n");

    // reverse array
    // for (int i = n-1; i >= 0; i--) {
    //     printf("%d ", arr[i]);
    // }

    // printf("\n");

    // add all the elements of the array
    // int sum = 0;
    // for (int i = 0; i < n; i++) {
    //     sum = sum + arr[i];
    // }
    
    // printf("sum of the elements: %d", sum);
    // printf("\n");

    // adding 2 arrays
    // s = n + m;
    // for (int i = 0; i < n; i++)
    // {
    //     b[i] = arr[i];
    // }
    // for (int i = 0; i < m; i++)
    // {
    //     b[i+n] = a[i];
    // }
    // for (int i = 0; i < s; i++)
    // {
    //     printf("%d", b[i]);
    // }
            
            // printf("\n");

    // seperate odd and even nos in an array and display them in an seperate array
    
    // for (int i = 0; i < n; i++)
    // {
    //     if (arr[i] % 2 == 0) 
    //     {   
    //         q[j] = arr[i];
    //         j++;
    //     } else {
    //         w[k] = arr[i];
    //         k++;
    //     }
        
    // }
    
    // for (int i = 0; i < j; i++)
    // {
    //     printf("%d", q[i]);
    // }

    // printf("\n");

    // for (int i = 0; i < k; i++)
    // {
    //     printf("%d", w[i]);
    // }

    printf("\n");

    // CODE TO PRINT THE ARRAY IN ASCENDING ORDER USING TEMP VARIABLE
    for (int i = 0; i < n; i++)
    {
        for (int j = i+1; j < n; j++)
        {
            if (arr[i] > arr[j]) {
                temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        
    }
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    

}