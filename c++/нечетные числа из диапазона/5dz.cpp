#include <iostream>

using namespace std;

int main() {
int start, end, summ = 0;
    cout << "Введите начало диапазона: ";
    cin >> start;
    cout << "Введите конец диапазона: ";
    cin >> end;
    
    if (start > end) {
        swap(start, end);
    }
    

cout << "Нечетные числа из этого диапазона: ";
for (int i = start; i <= end; i++){
    if (i % 2 != 0){
        summ += i;
        cout << i << " ";
    }
}
cout << endl << "Их сумма: " << summ;
    return 0;
}

