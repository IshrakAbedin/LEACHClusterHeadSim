from LEACHHeads import simulator, plotter

nodeCount = 100
rounds = 1000
densityOfHead = 0.05

sim = simulator(nodeCount, rounds, densityOfHead) # Creates new simulation
sim.runSimulation()
print(sim.getAverageHeadCountPerRound())
plotter.plotHeadHistory(sim)
plotter.plotPerNodeHeadCount(sim)
plotter.plotPerRoundHeadCount(sim)
plotter.showPlots()