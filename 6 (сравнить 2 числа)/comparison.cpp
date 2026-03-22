#include <iostream>
using namespace std;
int main () {
int a, b;
cin >> a >> b;
if (a == b) {
    cout << " числа a и b равны ";
}
else if (a > b){
    cout << " число a больше числа b ";
}
else if (a < b){
    cout << " число a меньше числа b ";
}
    return 0;
} 