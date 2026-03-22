#include <iostream>
using namespace std;

// вывод чисел от 1 до 19 словами
string get_1_to_19(int num) {
    string words[] = {"", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять",
                      "десять", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать",
                      "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"};
    return words[num];
}

// вывод десятков словами
string get_tens(int num) {
    string words[] = {"", "", "двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят",
                      "семьдесят", "восемьдесят", "девяносто"};
    return words[num];
}

// вывод сотен словами
string get_hundreds(int num) {
    string words[] = {"", "сто", "двести", "триста", "четыреста", "пятьсот", "шестьсот",
                      "семьсот", "восемьсот", "девятьсот"};
    return words[num];
}

// вывод тысяч словами
string get_thousands(int num) {
    string words[] = {"", "одна тысяча", "две тысячи", "три тысячи", "четыре тысячи",
                      "пять тысяч", "шесть тысяч", "семь тысяч", "восемь тысяч", "девять тысяч"};
    return words[num];
}

// окончания слова "рубль"
string get_currency_suffix(int num) {
    int last = num % 10;
    int last_two = num % 100;

    if (last_two >= 11 && last_two <= 19) {
        return "рублей";
    } else if (last == 1) {
        return "рубль";
    } else if (last >= 2 && last <= 4) {
        return "рубля";
    } else {
        return "рублей";
    }
}

int main() {
    int num;
    cout << "Введите сумму от 1 до 9999: ";
    cin >> num;

    if (num < 1 || num > 9999) {
        cout << "Ошибка! Введите число в диапазоне от 1 до 9999." << endl;
        return 1;
    }

    string result = "";

    // разбираем число на разряды
    int thousands = num / 1000;
    int hundreds = (num % 1000) / 100;
    int tens = (num % 100) / 10;
    int ones = num % 10;

    if (thousands > 0) {
        result += get_thousands(thousands) + " ";
    }
    if (hundreds > 0) {
        result += get_hundreds(hundreds) + " ";
    }
    if (tens == 1) {  // особый случай для чисел 11-19
        result += get_1_to_19(tens * 10 + ones) + " ";
    } else {
        if (tens > 1) {
            result += get_tens(tens) + " ";
        }
        if (ones > 0) {
            result += get_1_to_19(ones) + " ";
        }
    }

    // убираем лишний пробел в конце и добавляем валюту
    result += get_currency_suffix(num);
    cout << result << endl;
    return 0;
}