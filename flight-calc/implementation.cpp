#include "header.hpp"

#include <algorithm>
#include <iostream>
#include <cmath>

int change_in_altitude(int const &end_alt, int const &start_alt){
    if(start_alt > end_alt) {return start_alt-end_alt;} //descent
    return end_alt-start_alt; //ascent
}

int angle(int const &alt_chng, int const &distance) {
    return (alt_chng/distance)/100;
}

std::pair<int,int> fpm(int const &alt_chng, int const &distance, int const &speed) {
    auto pitch = (alt_chng/distance)/100;
    double time = (static_cast<double>(distance)/static_cast<double>(speed))*60;
    int fpm = alt_chng/time;
    fpm = static_cast<int>(std::round(fpm));
    std::pair<int,int> result{pitch, fpm}; //{pitch angle, fpm}
    return result;
}