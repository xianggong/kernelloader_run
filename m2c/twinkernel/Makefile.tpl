MAX_CYCLES = 400000
MIX_RATIO = $(shell basename $(CURDIR))

all: run

run:
	test ! -f sim.rpt && M2S_MIX_RATIO=0.$(MIX_RATIO) find -name "*.ini" -exec bash -c "$(M2SROOT)/bin/m2s --si-sim detailed --mem-report mem.rpt --si-debug-scheduler sched.rpt --si-max-cycles $(MAX_CYCLES) --si-report sim.rpt --si-config $(M2SROOT)/samples/southern-islands/7970/si-config --mem-config $(M2SROOT)/samples/southern-islands/7970/mem-config --opencl-debug stdout ../../../../../../build/loader/src/loader_m2s --logtostderr=1 --config={} > log 2>&1 " \;

see:
	test ! -f sim.rpt && M2S_MIX_RATIO=$(MIX_RATIO) find -name "*.ini" -exec $(M2SROOT)/bin/m2s --si-sim detailed --si-max-cycles $(MAX_CYCLES) --si-report sim.rpt --si-config $(M2SROOT)/samples/southern-islands/7970/si-config --mem-config $(M2SROOT)/samples/southern-islands/7970/mem-config ../../../../../../build/loader/src/loader_m2s --logtostderr=1 --config={} \;

emu:
	find -name "*.ini" -exec bash -c "$(M2SROOT)/bin/m2s --si-sim functional --si-debug-isa dbg.isa --si-debug-scheduler dbg.sch ../../../../../build/loader/src/loader_m2s --logtostderr=1 --config={} > log.emu 2>&1 " \;

half:
	test ! -f sim.rpt && M2S_MIX_RATIO=$(MIX_RATIO) find -name "*.ini" -exec bash -c "$(M2SROOT)/bin/m2s --si-max-ratio 0.5 --si-sim detailed --si-report sim.rpt --si-config $(M2SROOT)/samples/southern-islands/7970/si-config --mem-config $(M2SROOT)/samples/southern-islands/7970/mem-config ../../../../../build/loader/src/loader_m2s --logtostderr=1 --config={} > log 2>&1 " \;

seehalf:
	test ! -f sim.rpt && M2S_MIX_RATIO=$(MIX_RATIO) find -name "*.ini" -exec bash -c "$(M2SROOT)/bin/m2s --si-max-ratio 0.5 --si-sim detailed --si-report sim.rpt --si-config $(M2SROOT)/samples/southern-islands/7970/si-config --mem-config $(M2SROOT)/samples/southern-islands/7970/mem-config ../../../../../build/loader/src/loader_m2s --logtostderr=1 --config={}" \;

clean:
	rm -rf *output* *input* *log* cu* *rpt *dbg*

