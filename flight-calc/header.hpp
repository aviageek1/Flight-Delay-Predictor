#pragma once

//inputs into driver
//find delta altitude
//calculate rate of descent/climb

template <typename T>
T change_in_altitude(T const &end_alt, T const &start_alt){
    return start_alt-end_alt;
}

template <typename K>
K descent_change(K &alt_chng, K &distance) {
    return alt_chng/distance;
}

template <typename V>
V ascent_change(V &alt_chng, V &distance) {
    return alt_chng/distance;
}