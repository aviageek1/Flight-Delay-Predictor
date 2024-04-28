#pragma once

#include <vector>

int change_in_altitude(int const &end_alt, int const &start_alt);

int angle(int const &alt_chng, int const &distance);

std::pair<int,int> fpm(int const &alt_chng, int const &distance, int const &speed);
