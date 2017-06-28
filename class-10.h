/*
Gabriel Heikes
Section 730
Project 10
April 15, 2017
class-10.h
*/
#ifndef BISTACK_H
#define BISTACK_H

#include<iostream>
using std::ostream; 
#include<sstream>
using std::ostringstream;
#include<string>
using std::string;
#include<algorithm>
using std::copy;
#include<iterator>
using std::ostream_iterator;
#include<initializer_list>
using std::initializer_list;
#include<stdexcept>
using std::overflow_error; using std::underflow_error;

//Header member declared
template<typename T>
class BiStack{
private:
	size_t capacity_ = 4;
	size_t maximum_ = 16;
	size_t topside1=-1;
	size_t topside2;
	size_t size_;
	T *data_ = nullptr;
	void grow_and_copy();

public:
	BiStack(size_t cap=4, size_t max=16);
	BiStack(initializer_list<T>, size_t max=16);
	BiStack(const BiStack&);
	~BiStack();
	BiStack& operator= (const BiStack&);
	size_t size();
	size_t capacity();
	size_t max();
	bool empty1();
	bool empty2();
	void push1(T);
	void push2(T);
	T top1();
	T top2();
	void pop1();
	void pop2();
	
	
	//Inline cout overload, allows the data to be printed properly
	friend ostream& operator<<(ostream& out, const BiStack<T>& b){
		ostringstream oss1;
		string s;
		out << "Top1 ";
		if(b.topside1 < 1)
			out << "empty" << endl ;
		if(b.topside1 >= 1)
			out << "index:" << (b.topside1) << endl ;
		out << "Top2 ";
		if(b.topside2 == b.capacity_)
			out << "empty" << endl ;
		if(b.topside2 < b.capacity_)
			out << "index:" << (b.topside2) << endl;	
		for(unsigned int i=0; i<(b.capacity_); i++)
			oss1 << b.data_[i] << ",";
		s = oss1.str();
	  	s = s.substr(0, s.size()-1);
			
		out << "Size:" << b.size_ << endl << "Capacity:" << b.capacity_ << endl << s;
		return out;
	}
};

//Constructor for BiStack, with 2 arguments
template <typename T>
BiStack<T>::BiStack(size_t cap, size_t max){
	capacity_ = cap;
	maximum_ = max;
	topside1 = -1;
	topside2 = cap;
	size_ = 0;
	data_ = new T[cap];
}

//From Stack Dynamic Example
//Constructor for BiStack, with initialized list and max argument
template <typename T>
BiStack<T>::BiStack(initializer_list<T> lst, size_t mx){
	size_t sz = lst.size();
	data_ = new T[sz];
	capacity_ = sz;
	maximum_ = mx;
	topside1 = sz-1;
	topside2 = sz;
	size_ = sz;
	size_t index = 0;
	
	for(auto i : lst)
		data_[index++] = i;
}

//Constructor for BiStack, using a previous initialized BiStack
template <typename T>
BiStack<T>::BiStack(const BiStack<T> &b){
	capacity_ = b.capacity_;
	maximum_ = b.maximum_;
	size_ = b.size_;
	data_ = new T[b.capacity_];
	topside1 = b.topside1;
	topside2 = b.topside2;
	size_ = b.size_;
	std::copy(b.data_, b.data_+b.capacity_, data_);
}

//Overloads the assignment operator = to be able to set a BIStack equal to another BiStack
template <typename T>
BiStack<T>& BiStack<T>::operator= (const BiStack<T>& b){
	capacity_ = b.capacity_;
	maximum_ = b.maximum_;
	size_ = b.size_;
	data_ = new T[b.capacity_];
	topside1 = b.topside1;
	topside2 = b.topside2;
	size_ = b.size_;
	std::copy(b.data_, b.data_+b.capacity_, data_);
	return *this;
}

//From stackDynamic Template
//Destructor operator
template <typename T>
BiStack<T>::~BiStack(){
    delete [] data_;
}

//Returns the size of the Bistack
template <typename T>
size_t BiStack<T>::size(){
	size_t sz = size_;
	return sz;
}

//Returns the current size of the BiStack
template <typename T>
size_t BiStack<T>::capacity(){
	size_t cap = capacity_;
	return cap;
}

//Returns the maximum capacity of the BiStack
template <typename T>
size_t BiStack<T>::max(){
	size_t max =  maximum_;
	return max;
}

//Checks if the top1 of the BiStack is empty
template <typename T>
bool BiStack<T>::empty1(){
	return (topside1 == 0);
}

//Checks if the top1 of the BiStack is empty
template <typename T>
bool BiStack<T>::empty2(){
	return (topside2 == capacity_);
}

//Grows the capacity to allow more elements to be added
template <typename T>
void BiStack<T>::grow_and_copy(){
	T *new_data;
	//Throws error if the new capacity exceeds the max limit
	if((capacity_*2) > maximum_){
		throw overflow_error("stack past max");
	}
	else{
	//Creates a new chunk of data with double the capacity of the old one
		new_data = new T[capacity_ * 2] {};
		//Copies the data into the new bigger chunk of memory 
		std::copy(data_, data_+ topside1+1, new_data);
		std::copy(data_+topside2, data_+capacity_, new_data+(capacity_*2) - (capacity_-topside2));
		topside2 += capacity_;
		capacity_ *= 2;
		std::swap (new_data, data_);
		delete [] new_data;
	}
}

//Adds the new val into the top1 BiStack and runs the grow function is needed
template <typename T>
void BiStack<T>::push1(T val){
	if(size_ >= (capacity_))
		BiStack::grow_and_copy();
	topside1++;
	size_++;
	data_[topside1] = val;
}

//Adds the new val into the top2 BiStack and runs the grow function is needed
template <typename T>
void BiStack<T>::push2(T val){
	if(size_ >= (capacity_))
		BiStack::grow_and_copy();
	topside2--;
	size_++;
	data_[topside2] = val;	
}

//Returns the top2 value, throws error if empty
template <typename T>
T BiStack<T>::top1(){
	T tp;
	if(empty1())
		throw underflow_error("underflow stack 1");
	else
		tp = data_[topside1];
	return tp;
}

//Returns the top2 value, throws error if empty
template <typename T>
T BiStack<T>::top2(){
	T tp;
	if(empty2())
		throw underflow_error("underflow stack 2");
	else
		tp = data_[topside2];
	return tp;
}

//Removes the top1 value, throws error if empty
template <typename T>
void BiStack<T>::pop1(){
	if(!empty1()){
		topside1--;
		size_--;
	}
	else	
		throw underflow_error("underflow stack 1");
}

//Removes the top2 value, throws error if empty
template <typename T>
void BiStack<T>::pop2(){
	if(!empty2()){
		topside2++;
		size_--;
	}
	else	
		throw underflow_error("underflow stack 2");
}

#endif
