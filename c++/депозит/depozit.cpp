#include <iostream>
using namespace std;
int main() {
int depozit, mhran ;
cout << "Введите сумму депозита: ";
cin >> depozit;
cout << "Введите количество месяцев хранения денег в банке: ";
cin >> mhran;
int prvm, summpr, summ;
  prvm = (depozit * ( 5 / 100) / 365)* 30;
  summpr = prvm * mhran;
  summ = depozit + summpr;
 cout << " Прибыль с депозита в месяц: " << prvm << " руб." << endl;
 cout << " Прибыль за весь срок депозита: " << summpr << " руб." << endl;
 cout << " Общая сумма к выплате: " << summ << " руб." << endl;
    return 0;
}