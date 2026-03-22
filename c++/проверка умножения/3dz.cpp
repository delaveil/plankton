#include <iostream>
using namespace std;
int main(){

int a, b;
cout << " Введите два числа: ";
cin >> a >> b;

int r;
cout << " Введите результат их умножения: ";
cin >> r;

if (r == (a * b)){
    cout << "Ответ верный :)";
}
else {
    cout << " Пока неверно :(. Вот правильный ответ: " << (a * b);
}

    return 0;
}