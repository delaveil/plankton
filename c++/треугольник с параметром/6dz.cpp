#include <iostream>

using namespace std;

int main (){
int height;
cout << "Введите высоту треугольника: ";
cin >> height;

// i - номер строки
for (int i = 1; i <= height; i ++){
    // j - кол-во пробелов
    for (int j = 0; j < height - i; j++){
        cout << " ";
    }
    // a - колво *
    for (int a = 0; a < 2 * i - 1; a++) {
        cout << "*";
    }
cout << endl;
}
    return 0;
}