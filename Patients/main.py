import tool.controller as controller


def run() -> None:
    path = "./nativeData"
    patient_path = path + "./patients.csv"
    transfer_path = path + "./transfers.csv"
    file_name = "patient_release"
    controller.Patient(patient_path, transfer_path, file_name).run()


if __name__ == "__main__":
    run()
