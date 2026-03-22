#include <iostream>
using namespace std;
int main (){
int a, k = 0, s = 0;
cin >> a;
while (a != 0){
    k = k + 1;
    s = s + a;
    cin >> a;
}
cout << " Количество введенных чисел: " << k << endl;
cout << " Сумма введенных чисел: " << s << endl;
cout << " Среднее арифметическое введеных чисел: " << s / k << endl;
    return 0;
}