#include <iostream>
using namespace std;
int main(){
  int x, y;
  cout << "Введите координаты через пробел: ";
  cin >> x >> y;

  //0
  if (x == y && x == 0){
    cout << " 0 ";
  }
  //1 четверть
  else if (x > 0 && y > 0){
    cout << " 1 ";
}
     //между 1 и 2
     else if (x == 0 && y > 0){
        cout << " 1 " << " " << " 2 ";
}
//2 четверть
else if (x < 0 && y > 0){
    cout << " 2 ";
}
    //между 2 и 3
    else if (x < 0 && y == 0){
        cout << " 2 " << " " << " 3 ";
} 
  //3 четверть
  else if (x < 0 && y < 0){
    cout << " 3 ";
}
     //между 3 и 4
     else if (x == 0 && y < 0){
        cout << " 3 " << " " << " 4 ";
}
//4 четверть
else if (x > 0 && y < 0){
    cout << " 4 ";
}
     //между 4 и 1
     else if (x > 0 && y ==0){
       cout << " 4 " << " " <<  " 1 ";
}
    return 0;
}