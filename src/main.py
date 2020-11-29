import EESwrapper.wrapper as wrapper
import EESwrapper.InputParam as InputParam
from pathlib import Path
import constants



# Wrapper initialisation
EES2D = wrapper.wrapper(constants.EXEC_EULER2D_A)

# input parameter initialisation
# for i, res in enumerate([1e-3,1e-6,1e-9,1e-12,1e-15]):
#     input = InputParam.InputParam(meshFile=MESH_EULER_65x65,aoa=1.25,mach=1.5,maxIteration=int(1e5), minimumResidual=res)

#     sim = EES2D.RunSim(input,additionalArgs=["-vv"])

#     outputfolder = Path(".")/"etudeResiduSuper{:.0E}".format(res)
#     sim.move2folder(outputfolder)
#     sim.plotResiduals(outputfolder/"residuals.png")

#     sim.deleteFiles()

# input parameter initialisation

# time = []
for i, mesh in enumerate([constants.MESH_EULER_65x65]):
    input = InputParam.InputParam(meshFile=mesh,aoa=1.25,mach=0.8,maxIteration=int(1e7), minimumResidual=1e-14, cfl=0.25)

    sim = EES2D.RunSim(input,additionalArgs=["-vv"])
    sim.plotResiduals("test.png")

# print(time)