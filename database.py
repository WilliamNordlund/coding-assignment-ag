class Database:
    logs = [] 

    @staticmethod
    def store_log(log_entry):
        Database.logs.append(log_entry)
