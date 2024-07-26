#include <stdio.h>
#include <fstream>

#include "ap_int.h"
#include "params.hpp"

void compute
(
    ap_uint<WIDTH> in0,
    ap_uint<WIDTH> in1,
    #ifdef ADD
        ap_uint<WIDTH> *out
    #elif defined MUL 
        ap_uint<WIDTH> *out
    #endif
)
{
#pragma HLS INTERFACE ap_ctrl_none port=return
    #ifdef ADD
	    *out = in0 + in1;
    #elif defined MUL 
	    *out = in0 * in1;
    #endif
}
