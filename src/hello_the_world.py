from data import Point
from mpi4py import MPI 


SIZE = MPI.COMM_WORLD.Get_size()
RANK = MPI.COMM_WORLD.Get_rank()
COMM = MPI.COMM_WORLD

mydata = (RANK+1)**2
data = COMM.gather(mydata, root=0)
if RANK == 0:
  # for i in range(SIZE):
    #   assert data[i] == (i+1)**2
    pass
else:
   assert data is None

print "processor",RANK,'DATA',data