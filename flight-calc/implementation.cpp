#include "header.hpp"

#include <algorithm>
#include <iostream>
#include <cmath>



//used in both calculators
int change_in_altitude(int const &end_alt, int const &start_alt){
    if(start_alt > end_alt) {return start_alt-end_alt;} //descent
    return end_alt-start_alt; //ascent
}



//fpm and glideslope calculator functions
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



//top of descent calculator functions
int change_in_speed(int const &cruise_speed, int const &final_speed) {}

std::pair<int, int> tod(int const &alt_chng, int const &distance, int const &speed_chng, int const &fpm_or_pitch) {}