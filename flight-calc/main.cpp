#include "header.hpp"

#include <iostream>
#include <string>
#include <vector>
#include <iterator>
#include <algorithm>

int main() {
    std::string c_or_d;
    int start_alt, st_units;
    int end_alt, end_units;
    int distance, distance_units;

    bool repeat = true;

    std::cout << "-------Welcome to flight ascent/descent calculator-------" << std::endl;
    std::cout << "-----------------Made by Aayush Sharma:------------------" << std::endl;
    std::cout << std::endl;
    
    while(repeat) {
        std::cout << "Would you like find rate of climb (c) or descent (d)? Enter: ";
        std::cin >> c_or_d;
        std::cout << "Enter starting altitude and then units(mi,km,nm): ";
        std::cin >> start_alt >> st_units;
        std::cout << "Enter ending altitude and then units(mi,km,nm): ";
        std::cin >> end_alt >> end_units;
        std::cout << "Enter distance to target (i.e. DME/VOR) and then units(ft,m)";
        std::cin >> distance >> distance_units;
    }
    

}