#include <iostream>
using namespace std;


template<typename T> T get_sum(T num1,T num2){
    T num3 = num1 + num2;
    cout << num3 << endl;
    return num3;
}
int main(){
    get_sum(1, 2);
}