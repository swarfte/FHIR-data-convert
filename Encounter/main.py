import tool.controller as controller


def run() -> None:
    path = './nativeData'
    admissions_path = path + '/admissions.csv'
    transfers_path = path + '/transfers.csv'
    file_name = 'encounter_release'
    controller.Encounter(admissions_path, transfers_path, file_name).run()


if __name__ == '__main__':
    run()
