#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv)
{

struct timeval start, end;

gettimeofday(&end, NULL);

printf("%ld \n  %ld \n", end.tv_sec , end.tv_usec);

return 0;
}