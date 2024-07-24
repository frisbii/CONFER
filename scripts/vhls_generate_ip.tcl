cd $::env(PRJ_DIR)

open_project -reset $::env(PRJ_NAME)

add_files $::env(SRC_FILE) -cflags $::env(CFLAGS)
add_files $::env(HEADER_FILE)

set_top compute

open_solution "solution1"

set_part $::env(PART) -tool vivado
create_clock -period $::env(CLK_PERIOD) -name default
#source "./param-int-final/solution1/directives.tcl"

# TODO: proper testing should be set up
#csim_design
csynth_design
#cosim_design
export_design -flow syn -rtl verilog -format ip_catalog -version 1.0.0

exit
