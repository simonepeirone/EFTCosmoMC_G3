import sys, batchJob, fnmatch
try: import argparse
except:
    print 'use "module load" to load python 2.7'
    sys.exit()

class batchArgs():

        def __init__(self, desc='', importance=True, noBatchPath=False):
            self.parser = argparse.ArgumentParser(description=desc)
            if not noBatchPath: self.parser.add_argument('batchPath')
            self.importanceParameter = importance;

        def parseForBatch(self):
            if self.importanceParameter:
                self.parser.add_argument('--noimportance', action='store_true')
                self.parser.add_argument('--importance', nargs='*', default=None)
            self.parser.add_argument('--name', default=None, nargs='+')
            self.parser.add_argument('--param', default=None, nargs='+')
            self.parser.add_argument('--paramtag', default=None, nargs='1')
            self.parser.add_argument('--data', default=None, nargs='1')
            self.parser.add_argument('--datatag', default=None, nargs='1')

            self.args = self.parser.parse_args()
            self.batch = batchJob.readobject(self.args.batchPath)
            return (self.batch, self.args)

        def wantImportance(self, importanceTag):
            return self.args.importance is None or len(self.args.importance) == 0 or importanceTag in self.args.importance

        def jobItemWanted(self, jobItem):
            return not jobItem.isImportanceJob and (self.args.importance is None) or jobItem.isImportanceJob and self.wantImportance(jobItem.importanceTag)

        def nameMatches(self, jobItem):
            if self.args.name is None: return True
            for pat in self.args.name:
                if fnmatch.fnmatch(jobItem.name, pat): return True
            return False

        def dataMatches(self, jobItem):
            if self.args.datatag is None:
                if self.args.data is None: return True
                return self.args.data in jobItem.data_set
            else:
                return jobItem.datatag == self.args.datatag

        def paramsMatch(self, jobItem):
            if self.args.paramtag is None:
                if self.args.param is None: return True
                for pat in self.args.name:
                    if pat in jobItem.param_set: return True
                return False
            else:
                return jobItem.paramTag == self.args.paramtag

        def filteredBatchItems(self, wantSubItems=True):
            for jobItem in self.batch.items(wantImportance=not self.args.noimportance, wantSubItems=wantSubItems):
                if self.jobItemWanted(jobItem) and self.nameMatches(jobItem) and self.paramsMatch(jobItem): yield(jobItem)



