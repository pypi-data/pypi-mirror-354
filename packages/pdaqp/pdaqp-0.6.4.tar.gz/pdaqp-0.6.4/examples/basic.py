import numpy

H =  numpy.array([[1.5064, 0.4838], [0.4838, 1.5258]])
f = numpy.zeros((2,1))
F = numpy.array([[9.6652, 5.2115], [7.0732, -7.0879]])
A = numpy.array([[1.0, 0], [-1, 0], [0, 1], [0, -1]])
b = 2*numpy.ones((4,1));
B = numpy.zeros((4,2));

thmin = -1.5*numpy.ones(2)
thmax = 1.5*numpy.ones(2)

from pdaqp import MPQP
mpQP = MPQP(H,f,F,A,b,B,thmin,thmax)
mpQP.solve({'store_dual':True})
status = mpQP.codegen(max_reals=100)
print(status)
print(mpQP.solution_info.status)
print(str(mpQP.solution_info.status) == "Solved")
#mpQP.plot_regions()
#mpQP.plot_solution()
#mpQP.build_tree()
mpQP.codegen(dir="codegen", fname="pdaqp", dual=True,bfs=False, c_float_store="float", float_type="double")
