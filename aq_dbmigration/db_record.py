
class DBRecord(object):

    def __init__(self, id, sequence, version, description, file_path, install_time, execution_time, check_value):
        self.id = id
        self.sequence = sequence
        self.version = version
        self.description = description
        self.file_path = file_path
        self.install_time = install_time
        self.execution_time = execution_time
        self.check_value = check_value
        self.main_sequence = int(float(self.sequence))
        self.sub_sequence = int(self.sequence.split(".")[1]) if self.sequence.__contains__(".") else 0
        self.content = None

    @staticmethod
    def of_db(row):
        return DBRecord(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

    @staticmethod
    def of_file(sequence, version, description, file_path, check_value, content):
        record = DBRecord(None, sequence, version, description, file_path, None, None, check_value)
        record.content = content
        return record