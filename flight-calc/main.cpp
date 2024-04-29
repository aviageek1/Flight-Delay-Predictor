#include "header.hpp"
#include "implementation.cpp"

#include <iostream>
#include <string>
#include <vector>
#include <iterator>
#include <algorithm>

int main() {
    // std::string c_or_d;
    // char metric_or_not;
    char end_state;
    char tod_fpm;
    int start_alt, end_alt;
    int distance;
    int speed;

    // bool metric = false;

    std::cout << "-------Welcome to the flight ascent/descent calculator!-------" << std::endl;
    std::cout << "-----------------Made by Aayush Sharma------------------" << std::endl;
    std::cout << std::endl;

    std::cout << "Would you like the Top of Descent calculator (t) or Feet per Minute/Glideslope (f) calculator?: ";
    std::cin >> tod_fpm;
    // std::cout << "Would you like find rate of climb (c) or descent (d)? Enter: ";
    // std::cin >> c_or_d;
    // std::cout << "Would you like to use metric units? Default is customary units. (y or n): ";
    // std::cin >> metric_or_not;
    
    // if (metric_or_not == 'y') {metric = true;} //enable units

    //top of descent calculator    
    if (tod_fpm == 'f') {
        while (end_state == 'c') {
            std::cout << "Enter starting altitude: ";
            std::cin >> start_alt;
            std::cout << std::endl;
            
            std::cout << "Enter ending altitude: ";
            std::cin >> end_alt;
            std::cout << std::endl;
            
            std::cout << "Enter distance to target (i.e. DME/VOR): ";
            std::cin >> distance;
            std::cout << std::endl;
            
            std::cout << "Enter groundspeed (knots): ";
            std::cin >> speed;
            std::cout << std::endl;

            int alt_chng = change_in_altitude(start_alt, end_alt);
            std::pair<int,int> results = fpm(alt_chng, distance, speed);

            std::cout << "You need to maintain a " << results.second << " feet per minute level change at " << results.first << " degrees." << std::endl;
            std::cout << std::endl;
            std::cout << "Would you like to restart this calculator (c), switch to the Top of Descent calculator (s), or quit (q)?: ";
            std::cin >> end_state;
            if (end_state == 'c') {continue;}
        }
    }
    else if (tod_fpm == 't') {
        //add top of descent calculations
    }
    else {
        std::cout << "Invalid choice, continue (c) or quit (q)?: ";
        std::cin >> end_state;
        if (end_state == 'q') {
            exit(0);
        } else {
            std::cout << "Would you like the Top of Descent calculator (t) or Feet per Minute/Glideslope (f) calculator?: ";
            std::cin >> tod_fpm;
        }
    }
}