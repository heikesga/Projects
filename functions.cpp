/*
Gabriel Heikes
Section 730
Project 06
March 8, 2017
functions.cpp
*/
#include<iostream>
using std::cout; using std::cin; using std::endl;
#include<string>
using std::string;
#include<utility>
using std::pair;
#include<algorithm>
using std::copy;
#include<iterator>
using std::ostream_iterator;
#include<sstream>
using std::ostringstream;
#include<set>
using std::set;
#include <vector>
using std::vector;
#include "functions.h"

//Pulls in the text file and puts the data into a 2D vector
vector<vector<int>> readImage(int x, int y){
	vector<vector<int>> mat;
	int text;
	for(int i = 0; i < y; i++){
		vector<int> row;
		for(int j = 0; j < x; j++){
			cin >> text;
			(row).push_back(text);
		}
		mat.push_back(row);
	}
	return mat;
}

//Prints out the 2D vector
void printImage(vector<vector<int>> mat){
	int col = mat.size();
	for(int i=0; i < col; i++){
		int row = mat[i].size();
		for(int j=0; j < row; j++){
			cout << mat[i][j];
		}
		cout << endl;
	}
}

//Loops through the 2D vector in chuncks 2x2 and counts the number of 1s and 0s to determine the number of corners
int countHoles(vector<vector<int>> mat){
	int col = mat.size();
	int row = mat[0].size();
	int ex_ct, in_ct, fin_ct;
	for(int i=0; i < col-1; i++){
		for(int j=0; j < row-1; j++){
			if((mat[i][j]+mat[i+1][j]+mat[i][j+1]+mat[i+1][j+1])== 3){
				ex_ct++;
			}
			else if((mat[i][j]+mat[i+1][j]+mat[i][j+1]+mat[i+1][j+1])== 1){
				in_ct++;
			}
		}
	}
	fin_ct = (ex_ct - in_ct) / 4;
	return fin_ct;
}
