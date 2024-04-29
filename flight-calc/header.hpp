#pragma once

#include <vector>

//used in both calculators
int change_in_altitude(int const &end_alt, int const &start_alt);


//fpm/glideslope calculator functions
int angle(int const &alt_chng, int const &distance);
std::pair<int,int> fpm(int const &alt_chng, int const &distance, int const &speed);


//top of descent calculator functions
int change_in_speed(int const &cruise_speed, int const &final_speed);
std::pair<int, int> tod(int const &alt_chng, int const &distance, int const &speed_chng, int const &fpm_or_pitch);