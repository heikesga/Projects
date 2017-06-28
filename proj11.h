/*
Gabriel Heikes
Section 730
Project 11
April 23, 2017
proj11.h
*/
#ifndef PAL_H
#define PAL_H

#include<iostream>
using std::ostream; using std::cout; using std::endl;
#include<utility>
using std::swap;
#include<sstream>
using std::ostringstream;
#include<string>
using std::string;
#include<utility>
using std::pair;

// forward declaration so we can make Element a friend of PAL
template<typename T>
class PAL;

//node class
template <typename T>
class Element{
private:
  Element *next_ = nullptr;
  string name_ = "";
  T color_ = T();
  
public:
  Element()=default;
  Element(string name, T d) : next_(nullptr), name_(name), color_(d){};

  //From singlelink 18.2 example
  //Takes in the Node and returns it in a usable format
  friend ostream& operator<<(ostream& out, Element& n){
	out << n.name_ << ":" << n.color_;
	return out;
  };

    
  friend class PAL<T>;
};

//Templated class
template<typename T>
class PAL{
private:
  Element<T> *back_ = nullptr;
  Element<T> *front_ = nullptr;
  void print_list(ostream& out);  
public:
  PAL()=default;
  PAL(Element<T> n) : back_(&n), front_(&n) {};
  PAL(string n, T d);
  PAL(const PAL&);
  PAL& operator=(PAL);
  ~PAL();
  long count;
  void add(Element<T> &n);
  void add(string name, T dat);
  pair<Element<T>*, Element<T>*> find(string name);    
  pair<Element<T>*, Element<T>*> find(Element<T> &n);
  void move_forward1(Element<T> &n);
  void move_to_front(Element<T> &n);  
  void move_back1(Element<T> &n);
  void move_to_back(Element<T> &n);  

  //From example code 18.2
  //Inline function that prints the provide class
  friend ostream& operator<<(ostream& out, PAL<T>& el){
    el.print_list(out);
    return out;
  };
};

//From example code 18.2
//Prints the the nodes
template<typename T>
void PAL<T>::print_list(ostream& out){
	ostringstream oss;
	Element<T> *ptr;
	for(ptr = front_; ptr != nullptr; ptr = ptr->next_)
		oss << *ptr << ", ";
    string s = oss.str();
    //removes the comma and space at the end of the last element
    out << s.substr(0,s.size()-2);
}

//Constructor that takes in a name and the templated data
template<typename T>
PAL<T>::PAL(string name, T dat){
	Element<T>* ptr = new Element<T>(name, dat);
	back_ = ptr;
	front_ = ptr;
}

//From example code 18.2
//Copies the Node into a previous created node
template<typename T>
PAL<T>& PAL<T>::operator=(PAL p1){
	front_ = new Element<T>(p1.front_->name_, p1.front_->color_);
	back_ = front_;
	Element<T>* p1_ptr = p1.front_->next_;
	Element<T>* new_el;
	while (p1_ptr != nullptr){
		new_el = new Element<T>(p1_ptr->name_, p1_ptr->color_);
		back_->next_ = new_el;
		p1_ptr = p1_ptr->next_;
		back_ = new_el;
	}
	return *this;
}

//From example code 18.2
//Constructor that makes a new node if no info is provided
template<typename T>
PAL<T>::PAL(const PAL& p1){
	if(p1.front_ == nullptr){
		front_ = nullptr;
		back_ = nullptr;
	}
	else{
		front_ = new Element<T>(p1.front_->name_, p1.front_->color_);
		back_ = front_;
		Element<T>* p1_ptr = p1.front_->next_;
		Element<T>* new_el;
		while (p1_ptr != nullptr){
			new_el = new Element<T>(p1_ptr->name_, p1_ptr->color_);
			back_->next_ = new_el;
			p1_ptr = p1_ptr->next_;
			back_ = new_el;
		}
	}
}

//From example code 18.2
//Destructor
template<typename T>
PAL<T>::~PAL(){
    Element<T>* to_del = front_;
    while (to_del != nullptr){
	front_ = front_->next_;
	delete to_del;
	to_del = front_;
    }
    front_ = nullptr;
    back_ = nullptr;
}

//From example code 18.2
//Adds the provide data to the node
template<typename T>
void PAL<T>::add(Element<T> &n){
    if (front_ != nullptr){
		n.next_ = front_;
		front_ = &n;
    }
    else {
		front_=&n;
		back_=&n;
    }
}

//From example code 18.2
//Calls the previous add function
template<typename T>
void PAL<T>::add(string name, T dat){
	Element<T>* n = new Element<T>(name, dat);
	add(*n);
}

//Moves the target node forward one spot
template<typename T>
void PAL<T>::move_forward1(Element<T> &n){
	int cnt=0;
	Element<T> *node1 = nullptr;
	Element<T> *node2 = nullptr;
	for(Element<T> *el = front_; el != nullptr; el = el->next_){
		if(cnt==0){
			if(el->name_ == n.name_ ){
				node1 = el;
				cnt++;
			}
		}
		else if(cnt == 1){
			node2 = el;
			break;
		}
	}
	swap(node1->name_, node2->name_);
	swap(node1->color_, node2->color_);	
}

//Moves the targeted node to the front
template<typename T>
void PAL<T>::move_to_front(Element<T> &n){
	Element<T> *node = nullptr;
	for(Element<T> *el = front_; el != nullptr; el = el->next_){
		if(el->name_ == n.name_ ){
			node = el;
			break;
		}
	}
	swap(node->name_, back_->name_);
	swap(node->color_, back_->color_);
}

//Moves the target node backward one spot
template<typename T>
void PAL<T>::move_back1(Element<T> &n){
	Element<T> *node1 = nullptr;
	Element<T> *node2 = nullptr;
	for(Element<T> *el = front_; el != nullptr; el = el->next_){
		if(el->name_ != n.name_)
			node2 = el;
		else if(el->name_ == n.name_ ){
			node1 = el;
			break;
		}
	}
	swap(node1->name_, node2->name_);
	swap(node1->color_, node2->color_);
}

//Moves the targeted node to the back
template<typename T>
void PAL<T>::move_to_back(Element<T> &n){
	Element<T> *node = nullptr;
	for(Element<T> *el = front_; el != nullptr; el = el->next_){
		if(el->name_ == n.name_ ){
			node = el;
			break;
		}
	}
	swap(node->name_, front_->name_);
	swap(node->color_, front_->color_);
}

//From example code 18.2
//Finds the provided node and returns it in a pair with the node before it
template<typename T>
pair<Element<T>*, Element<T>*> PAL<T>::find(Element<T> &n){
	pair<Element<T>*, Element<T>*> p_node;
	Element<T> *node1 = nullptr;
	Element<T> *node2 = nullptr;
	//Loops through the nodes and finds the desired node and the one before it
	for(Element<T> *el = front_; el != nullptr; el = el->next_){
		if(el->name_ != n.name_)
			node2 = el;
		else if(el->name_ == n.name_ ){
			node1 = el;
			break;
		}
	}
	//Puts the 2 selected nodes into a pair then returns it
	p_node = make_pair(node1, node2);
	return p_node;
}

//From example code 18.2
//Finds the node from the name provided and returns it in a pair with the node before it
template<typename T>
pair<Element<T>*, Element<T>*> PAL<T>::find(string name){
	pair<Element<T>*, Element<T>*> p_node;
	Element<T> *node1 = nullptr;
	Element<T> *node2 = nullptr;
		//Loops through the nodes and finds the desired node and the one before it
	for(Element<T> *el = front_; el != nullptr; el = el->next_){
		if(el->name_ != name)
			node2 = el;
		else if(el->name_ == name){
			node1 = el;
			break;
		}
	}
	p_node = make_pair(node1, node2);
	return p_node;
};


#endif
