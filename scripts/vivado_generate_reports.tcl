set t1 [clock seconds]
puts {[TIMING] Vivado: Startup tasks}

open_project $::env(XPR_FILE)
update_compile_order -fileset sources_1
set_property STEPS.PHYS_OPT_DESIGN.IS_ENABLED true [get_runs impl_1]

puts [format "---> Approximate time taken: %f" [expr [clock seconds] - $t1]]
set t1 [clock seconds]
puts {[TIMING] Vivado: Implementation}

reset_run impl_1
launch_runs impl_1
wait_on_run impl_1
open_run impl_1

puts [format "---> Approximate time taken: %f" [expr [clock seconds] - $t1]]
set t1 [clock seconds]
puts {[TIMING] Vivado: Running reports}

report_utilization  -file $::env(UTIL_FILE)
report_timing       -file $::env(TIME_FILE)
report_power        -file $::env(POWER_FILE)

puts [format "---> Approximate time taken: %f" [expr [clock seconds] - $t1]]
set t1 [clock seconds]