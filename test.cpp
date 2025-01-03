#include <iostream>
using namespace std;

int main()
{
    int n = 9;
    int m = 12;

    for (int i = 1; i <= n; i++)
    {
        if (i % 2 != 0)
        {
            for (int j = 0; j < m; j++)
            {

                cout << "#";
            }
            cout << endl;
        }
        else
        {
            if (i % 4 == 0)
                cout << "#";
            for (int j = 0; j < m - 1; j++)
            {

                cout << ".";
            }
            if (i % 4 != 0)
                cout << "#";
            cout << endl;
        }
    }
    return 0;
}