
from ..schedule import * 
from ..reporting import * 
from ..ams.actions import * 
from ..ams import * 

class MakoDatabase(object):
    
    def __init__(self, **params):
        self.params = params
        if not self.validate():
            self.init()

    def getParams(self):
        return self.params

    def init(self):
        pass

    def validate(self):
        pass

    def uploadProjects(self, projects):
        pass

    def uploadMeasurementActions(self, actions):
        pass

    def uploadMeasurementData(self, action_id, data):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        pass

    def uploadData(self, data):
        """
        Data is list of tuples where first element is name and second concrete data 
        """
        pass

    def uploadSchedules(self, schedules):
        """
        schedules: list of Schedule objects:

        """
        pass

    def uploadReports(self, reports):
        pass

    def uploadDefaultConditions(self, conditions):
        pass

    def uploadTables(self, tables):
        pass

    def downloadProjects(self):
        pass

    def downloadMeasurementActions(self):
        pass

    def downloadMeasurementData(self, action_id):
        """
        data is list of tuples sorted by date from odler to newer

        first element in tuple is date 
        second element is value 
        """
        pass

    def downloadData(self):
        """
        Returns list of tuples where first element is name and second is data 
        """
        pass

    def downloadSchedules(self):
        """
        Returns list of Schedule object
        """
        pass

    def downloadReports(self):
        pass

    def downloadDefaultConditions(self):
        """
        Returns list of conditions for schedule
        """
        pass

    def downloadTables(self):
        pass

    def toDict(self):
        d = {}
        d["projects"] = [] 
        projects = self.downloadProjects()
        for project in projects:
            d["projects"].append(project.toDict())
        
        d["schedules"] = []
        schedules = self.downloadSchedules()
        for schedule in schedules:
            d["schedules"].append(schedule.toDict())

        d["default_conditions"] = []
        for condition in self.downloadDefaultConditions():
            d["default_conditions"].append(condition.toDict())

        metrics = self.downloadMeasurementActions()
        d["metrics"] = [] 
        d["data"] = []
        for metric in metrics:
            d["metrics"].append(metric.toDict())
            data = self.downloadMeasurementData(metric.getIdentifier())
            dd = {"id": metric.getIdentifier()}
            dd["data"] = [] 
            for val in data:
                dd["data"].append({"date": datetime.datetime.strftime(val[0], "%Y-%m-%d"), "value": val[1]})
            d["data"].append(dd)
        d["reports"] = [] 
        reports = self.downloadReports()
        for report in reports:
            d["reports"].append(report.toDict())

        d["tables"] = []
        tables = self.downloadTables()
        for table in tables:
            d["tables"].append(table.toDict())
        return d

    def fromDict(self, d):
        projects = []
        for project in d["projects"]:
            projects.append(ScheduleProject.fromDict(project))
        self.uploadProjects(projects)
        
        schedules = []
        for schedule in d["schedules"]:
            schedules.append(Schedule.fromDict(schedule))
        self.uploadSchedules(schedules)
        
        conditions = [] 
        for condition in d["default_conditions"]:
            conditions.append(ScheduleCondition.fromDict(condition))
        self.uploadDefaultConditions(conditions)
        
        ams = AMS()
        metrics = []
        for metric in d["metrics"]:
            metrics.append(ams.getAction(metric))
        self.uploadMeasurementActions(metrics)

        reports = []
        for report in d["reports"]:
            reports.append(Report.fromDict(report))
        self.uploadReports(reports)

        for data_obj in d["data"]:
            data = []
            for val in data_obj["data"]:
                data.append((datetime.datetime.strptime(val["date"], "%Y-%m-%d"), float(val["value"])))
            self.uploadMeasurementData(data_obj["id"], data)
        
        tables = [] 
        for table in d["tables"]:
            tables.append(Table.fromDict(table))
        self.uploadTables(tables)

    def export(self, db):
        """
        Exports data from current datatbase to database in argument 'db'

        This method also does validation and initialization of ndatabase 'db' if needed
        """
        db.uploadProjects(self.downloadProjects())
        actions = self.downloadMeasurementActions()
        db.uploadMeasurementActions(actions)
        for action in actions:
            db.uploadMeasurementData(action.getIdentifier(), self.downloadMeasurementData(action.getIdentifier()))
        db.uploadData(self.downloadData())
        db.uploadSchedules(self.downloadSchedules())
        db.uploadTables(self.downloadTables())
        db.uploadReports(self.downloadReports())
        db.uploadDefaultConditions(self.downloadDefaultConditions())
