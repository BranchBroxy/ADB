# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def init_function():
    import os
    from sys import platform

    if platform == "linux" or platform == "linux2":
        print("linux")
    elif platform == "darwin":
        print("darwin")
    elif platform == "win32":
        print("win32")
    if os.path.exists(os.path.join(os.getcwd(), "DrCell")) and os.path.isfile(os.path.join(os.getcwd(), "DrCell", "DrCell.m")):
        print("DrCell available")
    else:
        print("DrCell is not available")
        print("Downloading DrCell from GitHub")
        # https://pypi.org/project/directory-downloader/
        from git import Repo
        git_url = "https://github.com/biomemsLAB/DrCell"
        cwd = os.getcwd()
        directory = "DrCell"
        repo_dir = os.path.join(cwd, directory)
        Repo.clone_from(git_url, repo_dir)

    if os.path.exists(os.path.join(os.getcwd(), "SpikeDetectionAlgorithm")):
        print("Spike Detektion available")
    else:
        from git import Repo
        git_url = "https://github.com/flieb/SpikeDetection-Toolbox"
        cwd = os.getcwd()
        directory = "SpikeDetectionAlgorithm"
        repo_dir = os.path.join(cwd, directory)
        Repo.clone_from(git_url, repo_dir)

def get_list_of_files(path, file_type):
    """
        Generates a list with all file path from a given path.
        Parameters
        ----------
        path : string
            Either a path from a single file or a path of a directory.
        file_type : string, list of string
            The extension of the file type which should be taken into account.
            Can be one or more than one extension.

        Returns
        -------
        list_of_files : list of string
            Returns the synchrony of the input spike trains.

        """
    # from import_file import getListOfFiles
    import os
    all_files = []
    # check if path is a file or directory
    if os.path.isdir(path):
        all_files = getListOfFiles(path, file_type)
    else:
        all_files.append(path)
    return all_files

def getListOfFiles(dirName, file_extension):
    import os
    extension_list = []
    if isinstance(file_extension, str):
        extension_list.append(file_extension)
    if isinstance(file_extension, list):
        extension_list = file_extension
    # create a list of file and subdirectories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath, extension_list)
        else:
            name, extension = os.path.splitext(fullPath)
            if any(extension in s for s in extension_list):
            # if extension == file_extension:
                allFiles.append(fullPath)

    return allFiles

def import_dat(path):
    import pandas as pd
    # f = open(path)
    i = pd.read_csv(path, sep="\s+", encoding="cp1252", nrows=0)
    meta = list(i.columns.values)
    data = pd.read_csv(path, sep="\s+", encoding="cp1252", skiprows=3)
    return data, meta



def import_brw(path):
    import h5py
    import numpy as np
    import pandas as pd
    path = os.path.normpath(path)
    brw_data = h5py.File(path, 'r')
    brw_data_raw = brw_data["3BData/Raw"]
    print(brw_data)
    print(brw_data_raw)
    n_rec_frames = brw_data["/3BRecInfo/3BRecVars/NRecFrames"]
    n_rec_frames = int(n_rec_frames[0])
    print(n_rec_frames)
    NRows = brw_data["3BRecInfo/3BMeaChip/NRows"]
    NRows = int(NRows[0])
    NCols = brw_data["3BRecInfo/3BMeaChip/NCols"]
    NCols = int(NCols[0])
    NCh = NCols * NRows
    sa_ra = brw_data['/3BRecInfo/3BRecVars/SamplingRate']
    sa_ra = int(sa_ra[0])


    M = np.zeros(shape=(n_rec_frames, NCh))

    M = np.reshape(brw_data_raw, newshape=(NCh, n_rec_frames))
    M = M.transpose()
    df = pd.DataFrame(M)

    m = np.array(df[1])
    signal_inversion = brw_data['3BRecInfo/3BRecVars/SignalInversion']
    signal_inversion = int(signal_inversion[0])
    bit_depth = brw_data['3BRecInfo/3BRecVars/BitDepth']
    bit_depth = int(bit_depth[0])
    max_volt = brw_data['/3BRecInfo/3BRecVars/MaxVolt']
    max_volt = int(max_volt[0])
    m = signal_inversion * (m - (2 ** bit_depth) / 2) * (max_volt * 2 / 2 ** bit_depth)
    df_one = pd.DataFrame(m)
    print(df)
    return df_one, sa_ra
    print(M)
    """for name in path:
        yield name
"""
def matlab_apy(Selection, raw_data, sample_rate):
    import matlab.engine
    import os
    import numpy as np
    sample_rate = int(sample_rate)
    print("Starting MatLab APY")
    electrode = raw_data.reshape((raw_data.shape[0]))
    electrode = electrode.tolist()
    electrode = matlab.double(electrode)
    eng = matlab.engine.start_matlab()  # MatLab Umgebung aufrufen
    print("CD to MatLab")
    eng.cd("SpikeDetectionAlgorithm")
    path = os.path.normpath(r'C:\Users\phili\PycharmProjects\ADB\SpikeDetectionAlgorithm')
    print("Run MatLab APY")
    spike_train = eng.SD_adapter(path, Selection, electrode, sample_rate)
    eng.quit()
    # print(spike_train)
    return np.array(spike_train)



if __name__ == '__main__':
    import os
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    init_function()
    # df, sa_ra = import_brw(r"D:\Downloads\1P-LSD1_2ng_per_ml_TI-0.brw")
    data, meta = import_dat(r"D:\Downloads\Dat\0,125 Gy_6_Messung20.06.2019_09-08-44.dat")

    raw_signal = matlab_apy(Selection="genSpikes", raw_data=np.array([0, 2]), sample_rate=meta[2])
    # plt.plot(raw_signal)
    # plt.show()



    spike_train = matlab_apy(Selection="SWTEO", raw_data=raw_signal, sample_rate=10000)
    print(spike_train)
    print(type(spike_train))
    print(spike_train.shape)

    data = np.array(data.iloc[:, 1])
    spike_train1 = matlab_apy(Selection="SWTEO", raw_data=data, sample_rate=10000)
    print(spike_train1)
    print(type(spike_train1))
    print(spike_train1.shape)

    df = pd.DataFrame(spike_train)
    #plt.plot(spike_train)
    #plt.show()

    # plt.eventplot(spike_train)
    # plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
