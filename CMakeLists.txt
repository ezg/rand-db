cmake_minimum_required(VERSION 3.5)
project(rand_db)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall -Werror -g")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall -Werror -O3")

set(SOURCE_FILES main.cpp)
add_executable(rand_db ${SOURCE_FILES})