#include <iostream>
using namespace std;
int main (){
    int a;
cout << " введите порядковый номер пальца руки: ";
cin >> a;
if (a == 1) {
    cout << " это большой палец ";
}
else if (a == 2){
    cout << " это указательный палец ";
}
else if (a == 3){
    cout << " это средний палец ";
}
else if (a == 4){
    cout << " это безымяный палец ";
}
else if (a == 5){
    cout << " это мизинец ";
}
else if ( a > 5){
    cout << " у человека только 5 пальцев(( ";
}
    return 0;
}
