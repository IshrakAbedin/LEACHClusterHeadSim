import random
import matplotlib.pyplot as plt
from statistics import mean

class node:
    def __init__(self, identity, rounds : int, probability : float):
        self.identity = identity
        self.p = probability
        self.roundsLeft = 0
        self.becameHead = []
        self.headIndices = []
        for _ in range(rounds):
            self.becameHead.append(False)

    def tryBecomeHead(self, rnd : int) -> bool:
        if(self.roundsLeft > 0):
            self.roundsLeft -= 1
            return False
        else:
            chance = random.uniform(0, 1)
            tleft = rnd % round(1 / self.p) # Reelection
            t = self.p / (1 - self.p * tleft) #  threshold
            
            if(chance <= t):
                self.becameHead[rnd] = True
                self.headIndices.append(rnd)
                self.roundsLeft = int(1 / self.p - tleft) # Rounds left to be available for cluster head again
                return True
            else:
                return False

    def getTotalHeadCount(self) -> int:
        count = 0
        for i in self.becameHead:
            if i:
                count += 1

        return count

class simulator:
    def __init__(self, nodeCount : int, rounds : int, probability : float):
        self.nodeCount = nodeCount
        self.rounds = rounds
        self.probability = probability
        self.nodes = []
        self.simulated = False
        for i in range(nodeCount):
            self.nodes.append(node(i, rounds, probability))

    def runSimulation(self):
        for rnd in range(self.rounds):
            for i in range(self.nodeCount):
                self.nodes[i].tryBecomeHead(rnd)
        self.simulated = True

    def getHeadCountPerRound(self) -> list:
        if self.simulated:
            perRoundHeadCountList = []
            for rnd in range(self.rounds):
                count = 0
                for nd in self.nodes:
                    if nd.becameHead[rnd]:
                        count += 1
                perRoundHeadCountList.append(count)
            return perRoundHeadCountList
        else:
            print('Simulation has not been simulated yet. Try running simulator.runSimulation() method first.')
            return []

    def getAverageHeadCountPerRound(self) -> float:
        HeadCountPerRoundList = self.getHeadCountPerRound()
        if HeadCountPerRoundList != None:
            return mean(HeadCountPerRoundList)
        else:
            return -1
            
class plotter:
    @staticmethod
    def plotHeadHistory(simulation : simulator):
        if simulation.simulated:
            nodes = simulation.nodes
            plt.figure()
            index = 0
            for nd in nodes:
                x = nd.headIndices
                y = [index for _ in range(len(x))]
                plt.plot(x, y, '.')
                index += 1
            plt.title('Head History Per Node')
            plt.xlabel('Rounds')
            plt.ylabel('Nodes')
            plt.grid(True, which='both')
        else:
            print('Simulation has not been simulated yet. Try running simulator.runSimulation() method first.')

    @staticmethod
    def plotPerRoundHeadCount(simulation : simulator):
        if simulation.simulated:
            nodes = simulation.nodes
            rounds = simulation.rounds
            plt.figure()
            perRoundHeadCountList = []
            for rnd in range(rounds):
                count = 0
                for nd in nodes:
                    if nd.becameHead[rnd]:
                        count += 1
                perRoundHeadCountList.append(count)
            x = [i for i in range(rounds)]
            plt.bar(x, perRoundHeadCountList)
            plt.title('Head Count Per Round')
            plt.xlabel('Rounds')
            plt.ylabel('Total Head Count')
            plt.grid(True, which='major')
        else:
            print('Simulation has not been simulated yet. Try running simulator.runSimulation() method first.')

    @staticmethod
    def plotPerNodeHeadCount(simulation : simulator):
        if simulation.simulated:
            nodes = simulation.nodes
            nodeCount = simulation.nodeCount
            plt.figure()
            x = [i for i in range(nodeCount)]
            y = []
            for nd in nodes:
                y.append(nd.getTotalHeadCount())
            plt.bar(x, y)
            plt.title('Head Count Per Node')
            plt.xlabel('Nodes')
            plt.ylabel('Total Head Count')
            plt.grid(True, which='major')
        else:
            print('Simulation has not been simulated yet. Try running simulator.runSimulation() method first.')

    @staticmethod
    def showPlots():
        plt.show()

