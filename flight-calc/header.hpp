#pragma once

#include <vector>

template <typename T>
T change_in_altitude(T const &end_alt, T const &start_alt){
    if(start_alt > end_alt) {return start_alt-end_alt;} //descent
    return end_alt-start_alt; //ascent
}

template <typename V>
V angle(V const &alt_chng, V const &distance) {
    return (alt_chng/distance)/100;
}

template <typename K>
std::pair<K,K> fpm(K const &alt_chng, K const &distance, int const &speed) {
    auto pitch = (alt_chng/distance)/100;
    int mpm = speed/60;
    K fpm = pitch*mpm*100;
    std::pair<K,K> result{pitch, fpm}; //{pitch angle, fpm}
    return result;
}
