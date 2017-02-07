#include "testlib.h"
#include <iostream>

using namespace std;

int main(int argc, char* argv[])
{
    registerGen(argc, argv, 1);
    int tc = 100000;
//    cout << tc << endl;
    while(tc--){
        char gender = 'F';
        int a = rnd.next(120, 180);
        int b = rnd.next(50, 120);
        int c = rnd.next(3, 100);
        int d = rnd.next(0, 1);
        if(d){
            gender = 'M';
            a = rnd.next(200, 250);
        }
        cout << a << " " << b << " " << c << " " << gender << endl;

   }
   return 0;
}