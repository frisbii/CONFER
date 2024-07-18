#ifndef _PARAMS_H_
#define _PARAMS_H_

#include <cmath>

// ==============
// ALL FORMATS

// Define 4 as the default width if none is passed
#ifndef WIDTH
	#define WIDTH 4
#endif

// Define add as the default operator to implement if none is passed
#if !defined ADD && !defined MUL
	#define ADD
#endif

// ==============

// ===============
// FIXED POINT:

#ifndef INT_BITS
	#define INT_BITS (WIDTH / 2)
#endif

// ===============

#endif